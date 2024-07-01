import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_USER = os.getenv("SUPABASE_USER")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")
SUPABASE_HOST = os.getenv("SUPABASE_HOST")
SUPABASE_PORT = os.getenv("SUPABASE_PORT")
SUPABASE_DATABASE = os.getenv("SUPABASE_DATABASE")


def connect():
    try:
        connection = psycopg2.connect(
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            database=SUPABASE_DATABASE
        )
        print("Conexão estabelecida com sucesso.")
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise