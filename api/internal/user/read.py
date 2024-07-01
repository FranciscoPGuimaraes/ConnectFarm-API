from typing import List, Optional
from fastapi import HTTPException
from psycopg2 import IntegrityError

from api.internal.db import connect
from api.models.UserModels import UserOut


async def get_all_users() -> Optional[List[UserOut]]:
    query = """
            SELECT u.name, u.birth, u.phone, u.email, u.cpf
            FROM "user" as u;
            """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    users: List[UserOut] = []
                    for result in results:
                        users.append(UserOut(name=result[0], birth=result[1], phone=result[2], email=result[3], cpf=result[4]))
                        
                    return users
                else:
                    return None
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

async def get_user_by_cpf(cpf: str) -> UserOut:
    query = """
            SELECT u.name, u.birth, u.phone, u.email
            FROM user u where u.cpf = %(cpf)s;
            """
    try:
        with db_connect.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (cpf,))
                result = cursor.fetchall()

                if result:
                    user: UserOut
                    user = UserOut(name=result[0], birth=result[1], phone=result[2], email=result[3], cpf=result[4])

                    return user
                else:
                    return None
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()
