from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, File, UploadFile
from pydantic import BaseModel
import alumne
from alumne import alumne_schema
from alumne import alumne_sch2_list
from aula import aules_alumnes_schema
import db_alumne
import db_aula
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo Pydantic para los datos de un alumno
class student(BaseModel):
    IdAlumne: int
    IdAula: int
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    CreatedAt: int
    UpdatedAt: int

class tablaAlumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    DescAula: int

# Endpoint para listar todos los alumnos
@app.get("/alumne/list", response_model=List[tablaAlumne])
async def read_alumnes(
    orderby: Optional[str] = Query(None, regex="^(asc|desc)$"),
    contain: Optional[str] = None,
    skip: Optional[int] = Query(0, ge=0, le=100),
    limit: Optional[int] = Query(10, ge=1, le=100)
):
    # Llama a la función para obtener alumnos
    adb = db_alumne.read_list(orderby, contain, skip, limit)

    try:
        # Llama a la función para obtener alumnos
        alumnes_sch = alumne_sch2_list(adb)
    except ValueError as e:
        # Maneja errores si los datos no son válidos
        raise HTTPException(status_code=500, detail=str(e))
    return alumnes_sch

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    try:
        contents = await file.read()
        decoded_contents = contents.decode('utf-8')
        fieldnames = ['DescAula','Edifici','Pis','IdAula','NomAlumne','Cicle','Curs','Grup']
        reader = csv.DictReader(decoded_contents.splitlines(), fieldnames=fieldnames)
        alumnes = [row for row in reader]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo CSV: {e}")
    
    mensajes = []
    for alumne in alumnes:
        try:
            print("Procesando alumno:", alumne)
            db_aula.create(
                DescAula=int(alumne['DescAula']),
                Edifici=int(alumne['Edifici']),
                Pis=int(alumne['Pis'])
            )
            create_result = db_alumne.create(
                IdAula=int(alumne['IdAula']),
                NomAlumne=alumne['NomAlumne'],
                Cicle=alumne['Cicle'],
                Curs=int(alumne['Curs']),
                Grup=alumne['Grup']
            )
            if create_result.get("status") == -1:
                mensajes.append(f"Error: {create_result['message']} para el alumno {alumne['NomAlumne']}")
            else:
                mensajes.append(f"Éxito: Alumno {alumne['NomAlumne']} creado exitosamente.")
        except KeyError as e:
            mensajes.append(f"Error: Clave {str(e)} no encontrada en el CSV.")
        except Exception as e:
            mensajes.append(f"Error: {str(e)}")

    return {"message" : mensajes}

# Endpoint para mostrar detalles de un alumno específico por ID
@app.get("/alumne/show/{id}", response_model=dict)
async def show_alumne(id: int):
    alumne = db_alumne.read_id(id)
    print(f"Resultado de read_id: {alumne}")

    if isinstance(alumne, dict) and alumne.get("status") == -1:
        raise HTTPException(status_code=404, detail=alumne["message"])

    if isinstance(alumne, tuple):
        # Convierte la tupla a un diccionario para manejarlo mejor
        alumne = alumne_schema(alumne)
        print(f"Convertido a dict: {alumne}")
    else:
        raise HTTPException(status_code=404, detail="No existe este alumno")

    return alumne

# Endpoint para crear un nuevo alumno
@app.post("/alumne/add")
async def create_alumne(data:student):
    idaula = data.IdAula
    nomalumne = data.NomAlumne
    cicle = data.Cicle
    curs = data.Curs
    grup = data.Grup
    l_student_id = db_alumne.create(idaula,nomalumne,cicle,curs,grup)
    if idaula > 5 or idaula < 1:
        raise HTTPException(status_code = 404, detail = "IdAula no encontrado; ¡Utiliza un Aula entre 1 y 5!")
    return{
        "msg": "S'ha afegit correctament",
        "id alumne": l_student_id,
        "Nom Alumne" : nomalumne
    }

# Endpoint para actualizar un alumno existente
@app.put("/alumne/update/{id}", response_model=List[dict])
async def update_alumne(id:int, data: student):
    alumne = db_alumne.read_id(id)
    print(f"Resultado de read_id: {alumne}")
    
    if isinstance(alumne, dict):
        print(f"Claves de alumne: {alumne.keys()}")

    if alumne.get("status") == -1:
        message = alumne.get("message", "No existe este alumno")
        print(f"Detalle de error: {message}")
        raise HTTPException(status_code=404, detail=message)
    
    if data.IdAula > 5 or data.IdAula < 1:
        raise HTTPException(status_code=400, detail="IdAula fuera de rango;¡Utiliza un Aula entre 1 y 5!")
    
    result = db_alumne.update(data.IdAula, data.NomAlumne, data.Cicle, data.Curs, data.Grup, id)
    print(f"Resultado de update: {result}")

    if result.get("status") == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return result

# Endpoint para eliminar un alumno específico por ID
@app.delete("/alumne/delete/{id}", response_model=dict)
async def delete_alumne(id: int):
    alumne = db_alumne.read_id(id)
    print(f"Resultado de read_id: {alumne}")

    if isinstance(alumne, dict) and alumne.get("status") == -1:
        raise HTTPException(status_code=404, detail=alumne["message"])

    if isinstance(alumne, tuple):
        # Convierte la tupla a un diccionario para manejarlo mejor
        alumne = alumne_schema(alumne)
        print(f"Alumno a eliminar: {alumne}")
    else:
        raise HTTPException(status_code=404, detail="No existe este alumno")

    result = db_alumne.delete(id)
    print(f"Resultado de delete: {result}")

    if result.get("status") == -1:
        raise HTTPException(status_code=500, detail=result["message"])

    return {"msg": "Alumno eliminado correctamente"}

# Endpoint para listar todos los alumnos con sus respectivas aulas
@app.get("/alumne/listAll", response_model=List[dict])
async def list_all_alumnes():
    alumnes_classes = db_aula.read_all()
    try:
        alumnes_sch = aules_alumnes_schema(alumnes_classes)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not isinstance(alumnes_sch, list):
        raise HTTPException(status_code=500, detail="Error procesando datos de alumnos y aulas")

    return alumnes_sch