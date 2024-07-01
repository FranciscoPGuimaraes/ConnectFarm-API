import re
from fastapi import HTTPException
from psycopg2 import IntegrityError

from api.services.db import connect
from api.models.UserModels import UserIn


async def create_user(user: UserIn) -> None:
    query = """INSERT INTO "user"(cpf, name, email, password, phone, birth) VALUES (%(cpf)s, %(name)s, %(email)s, %(password)s, %(phone)s, %(birth)s);"""
    parameters = {
        'cpf': user.cpf,
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'phone': user.phone,
        'birth': user.birth,
    }
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
            conn.commit()

    except IntegrityError as e:
        error = re.search(r'Key \((.*?)\)=\((.*?)\) already exists', e.pgerror)
        raise HTTPException(status_code=400, detail=f"User with {error.group(1)} {error.group(2)} already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()