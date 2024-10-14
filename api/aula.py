# Función para transformar los datos de un aula a un diccionario
def aula_schema(classroom) -> dict:
    if len(classroom) < 6:
        return {"status": -1, "message": "Datos incompletos"}
    return {"IdAula": classroom[0],
            "DescAula": classroom[1],
            "Edifici": classroom[2],
            "Pis": classroom[3],
            "CreatedAt": classroom[4],
            "UpdatedAt": classroom[5]
            }

# Función para transformar los datos combinados de un estudiante y su aula a un diccionario
def aula_alumne_schema(student_class) -> dict:
    if len(student_class) < 11:
        return {"status": -1, "message": "Datos incompletos"}
    return {
        "IdAlumne": student_class[0],
        "IdAula": student_class[1],
        "NomAlumne": student_class[2],
        "Cicle": student_class[3],
        "Curs": student_class[4],
        "Grup": student_class[5],
        "CreatedAt": student_class[6],
        "UpdatedAt": student_class[7],
        "DescAula": student_class[8],
        "Edifici": student_class[9],
        "Pis": student_class[10]
    }

# Función para transformar una lista de datos combinados de estudiantes y aulas a una lista de diccionarios
def aules_alumnes_schema(alumnes_classes) -> list:
    alumnes_classes_list = []
    for alumne_class in alumnes_classes:
        schema = aula_alumne_schema(alumne_class)
        if "status" in schema and schema["status"] == -1:
            continue    # Omitir datos incompletos
        alumnes_classes_list.append(schema)
    return alumnes_classes_list