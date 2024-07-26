import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

def connect_mongo(collection_name: str) -> tuple[Collection, MongoClient]:
    try:
        client = MongoClient(MONGO_URI)
        db: Database = client['ConnectFarm']
        collection: Collection = db[collection_name]
        print("Conexão estabelecida com sucesso.")
        return collection, client
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise
