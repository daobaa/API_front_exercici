from client import db_client

# Función para leer todos los registros de la tabla AULA
def read():
    try:
        conn = db_client()  # Conectar a la base de datos
        cur = conn.cursor() # Crear un cursor para ejecutar consultas
        cur.execute("SELECT * FROM AULA")   # Ejecutar la consulta para seleccionar todos los registros de AULA
    
        students = cur.fetchall()   # Obtener todos los registros resultantes
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" } # Manejar errores de conexión y consultas
    finally:
        conn.close()    # Cerrar la conexión a la base de datos
    return students # Retornar los registros obtenidos

# Función para leer todos los registros de la tabla ALUMNE junto con la información de sus respectivas aulas
def read_all():
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
        SELECT ALUMNE.*, AULA.DescAula, AULA.Edifici, AULA.Pis 
        FROM ALUMNE
        JOIN AULA ON ALUMNE.IdAula = AULA.IdAula
        """# Consulta para seleccionar todos los registros de ALUMNE y unirlos con los de AULA
        cur.execute(query)
        students_classes = cur.fetchall()
    except Exception as e:
        print(f"Error de conexión: {e}")
        return []   # Retornar una lista vacía en caso de error
    finally:
        conn.close()
    return students_classes

def create(DescAula,Edifici,Pis):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT INTO AULA (DescAula, Edifici, Pis) VALUES (%s, %s, %s)"
        values = (DescAula, Edifici, Pis)
        cur.execute(query, values)
        
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close()
    return {"status": 1, "message": "Aula creada exitosamente"}