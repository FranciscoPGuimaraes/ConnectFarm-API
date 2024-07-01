from fastapi import HTTPException
from psycopg2 import IntegrityError

from api.internal.db import connect
from api.models.UserModels import Userin


async def create_user(user: Userin) -> None:
    query = """INSERT INTO "user"(cpf, name, email, password, phone, birth) VALUES (%(cpf)s, %(name)s, %(email)s, %(password)s, %(phone)s, %(birth)s);"""
    parameters = user.model_dump()
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                print(query)
                print(parameters)
                cursor.execute(query, parameters)
            conn.commit()

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Advisor with email {user.cpf} already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()