# Función para transformar los datos de un alumno a un diccionario
def alumne_schema(student) -> dict:
    if len(student) < 8:
        print(f"Datos incompletos en la fila del estudiante: {student}")    # Imprimir mensaje de datos incompletos para depuración
        return {"status": -1, "message": "Datos incompletos"}   # Manejar datos incompletos
    return {"IdAlumne": student[0],
            "IdAula": student[1],
            "NomAlumne": student[2],
            "Cicle": student[3],
            "Curs": student[4],
            "Grup": student[5],
            "CreatedAt": student[6],
            "UpdatedAt": student[7]
            }

# Función para transformar una lista de datos de alumnos a una lista de diccionarios
def alumnes_schema(alumnes) -> list:
    alumnes_list = []
    for alumne in alumnes:
        schema = alumne_schema(alumne)
        if "status" in schema and schema["status"] == -1:
            print(f"Datos incompletos en la fila: {alumne}")    # Imprimir mensaje de datos incompletos para depuración
            continue    # Omitir datos incompletos
        alumnes_list.append(schema)
    return alumnes_list

def alumne_sch2(fetchAlumnes) -> dict:
    if len(fetchAlumnes) > 5:
        return {"status": -1, "message": "Datos incompletos"}
    return {"NomAlumne": fetchAlumnes[0],
            "Cicle": fetchAlumnes[1],
            "Curs": fetchAlumnes[2],
            "Grup": fetchAlumnes[3],
            "DescAula": fetchAlumnes[4]
            }

def alumne_sch2_list(alumnos) -> dict:
    alumnes_list = []
    for alumne in alumnos:
        schema = alumne_sch2(alumne)
        if "status" in schema and schema["status"] == -1:
            continue
        alumnes_list.append(schema)
    return alumnes_list