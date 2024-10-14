import mysql.connector

# Función para establecer una conexión con la base de datos
def db_client():
    try:
        dbname = "alumnat"  # Nombre de la base de datos
        user = "root"   # Usuario de la base de datos
        password = "root"   # Contraseña del usuario
        host = "localhost"  # Host donde se encuentra la base de datos
        port = "3306"   # Puerto utilizado para la conexión
        collation = "utf8mb4_general_ci"    # Collation utilizado para la base de datos
        
        # Establecer la conexión con la base de datos utilizando los parámetros anteriores
        return mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = dbname,
            collation = collation
        ) 
            
    except Exception as e:
            # Manejar cualquier error que ocurra durante la conexión y retornar un mensaje de error
            return {"status": -1, "message": f"Error de connexió:{e}" }