from app.database import engine

try:
    connection = engine.connect()

    print ("Conectado com sucesso")
    
    connection.close()

except Exception as error:
    print(error)