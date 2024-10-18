from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import alumne
from alumne import alumne_schema
from alumne import alumne_sch2_list
from aula import aules_alumnes_schema
import db_alumne
import db_aula
from fastapi.middleware.cors import CORSMiddleware

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
    contain: Optional[str] = None
):
    # Llama a la función para obtener alumnos
    adb = db_alumne.read_list(orderby, contain)

    try:
        # Llama a la función para obtener alumnos
        alumnes_sch = alumne_sch2_list(adb)
    except ValueError as e:
        # Maneja errores si los datos no son válidos
        raise HTTPException(status_code=500, detail=str(e))
    return alumnes_sch

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