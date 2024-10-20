from typing import Optional
from client import db_client

# Función para leer todos los registros de la tabla ALUMNE
def read():
    try:
        conn = db_client()  # Conectar a la base de datos
        cur = conn.cursor() # Crear un cursor para ejecutar consultas
        cur.execute("SELECT * FROM ALUMNE") # Ejecutar la consulta para seleccionar todos los registros
        students = cur.fetchall()   # Obtener todos los registros resultantes
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" } # Manejar errores de conexión y consultas
    finally:
        conn.close() # Cerrar la conexión a la base de datos
    return students # Retornar los registros obtenidos

# Función para leer un registro específico de la tabla ALUMNE por ID
def read_id(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM ALUMNE WHERE IdAlumne = %s"  # Consulta para seleccionar un registro específico
        value = (id,)
        cur.execute(query,value)
    
        student = cur.fetchone()
        if student is None:
            return {"status": -1, "message": f"Error de connexió:{e}"}  # Manejar el caso en que no se encuentra el registro
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()
    return student

# Función para crear un nuevo registro en la tabla ALUMNE
def create(IdAula,NomAlumne,Cicle,Curs,Grup):
    if name_exists(NomAlumne):
        print(f"El nombre del alumno {NomAlumne} ya existe en la base de datos.")
        return {"status": -1, "message": "Este alumno ya existe en la base de datos."}
    
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT into ALUMNE (IdAula,NomAlumne,Cicle,Curs,Grup) VALUES (%s,%s,%s,%s,%s)" # Consulta de inserción
        values = (IdAula,NomAlumne,Cicle,Curs,Grup)
        cur.execute(query,values)

        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}
    finally:
        conn.close()
    return {"status": 1, "message": "Alumno creado exitosamente"}

# Función para actualizar un registro específico en la tabla ALUMNE por ID
def update(IdAula,NomAlumne,Cicle,Curs,Grup,id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "UPDATE ALUMNE SET IdAula = %s, NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s WHERE IdAlumne = %s"   # Consulta de actualización
        values = (IdAula,NomAlumne,Cicle,Curs,Grup, id)
        cur.execute(query,values)

        conn.commit()

    except Exception as e:
        print(f"Error de conexión:{e}")
        return {"status": -1, "message": f"Error de connexió:{e}"}
    finally:
        conn.close()
    return {"msg" : "Se ha actualizado correctamente", "id alumno" : id}    # Confirmar la actualización

# Función para eliminar un registro específico de la tabla ALUMNE por ID
def delete(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM ALUMNE WHERE IdAlumne = %s"    # Consulta de eliminación
        value = (id,)
        cur.execute(query, value)
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close()
    return {"status": 1, "message": "Alumno eliminado correctamente"}   # Confirmar la eliminación

def read_list(
        orderby: Optional[str] = None, 
        contain: Optional[str] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None
    ):
    try:
        conn = db_client()  # Conectar a la base de datos
        cur = conn.cursor() # Crear un cursor para ejecutar consultas
        base_query = """
        SELECT alu.NomAlumne, alu.Cicle, alu.Curs, alu.Grup, aul.DescAula
        FROM ALUMNE alu INNER JOIN AULA aul ON aul.IdAula = alu.IdAula
        """
        if contain:
            base_query += f" WHERE alu.NomAlumne LIKE '%{contain}%'" #Orden de filtrado por contenido del nombre
        if orderby:
            base_query += f" ORDER BY alu.NomAlumne {orderby}" #Orden de ordenar en caso de orderby
        if limit:
            base_query += f" LIMIT {limit}" #Orden de limitar el numero indicado de filas
        if skip:
            base_query += f" OFFSET {skip}" #Orden de saltar el numero indicado de filas
        
        cur.execute(base_query) # Ejecutar la consulta para seleccionar todos los registros
        students = cur.fetchall()   # Obtener todos los registros resultantes
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" } # Manejar errores de conexión y consultas
    finally:
        conn.close() # Cerrar la conexión a la base de datos
    return students # Retornar los registros obtenidos

def name_exists(NomAlumne):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT COUNT(*) FROM ALUMNE WHERE NomAlumne = %s"
        cur.execute(query, (NomAlumne,))
        result = cur.fetchone()
        print(f"Verificación de existencia del nombre {NomAlumne}: {result[0]}")
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close()
    return result[0] > 0  # Devuelve True si el nombre existe, False de lo contrario