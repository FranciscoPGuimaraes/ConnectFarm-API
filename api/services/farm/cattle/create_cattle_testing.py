from api.services.db import connect_mongo

async def create_cattle():
    collection, client = connect_mongo("cattles")
    try:
        result = collection.insert_one({"teste": "testado"})
        print(f"Dados inseridos com sucesso. ID do documento: {result.inserted_id}")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        client.close()
        print("Conexão fechada com sucesso.")