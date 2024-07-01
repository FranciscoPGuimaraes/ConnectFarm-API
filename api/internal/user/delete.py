from fastapi import HTTPException

from api.internal.db import connect


async def delete_team(cpf: str):
    try:
        delete_user = "DELETE FROM user WHERE cpf = %s"
        with connect.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(delete_user, (cpf,))
                conn.commit()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))