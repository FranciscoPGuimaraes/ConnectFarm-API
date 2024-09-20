import re
from uuid import UUID
from fastapi import HTTPException
from psycopg2 import IntegrityError

from api.services.db import connect
from api.models.AnnotationsModels import Annotations


async def create_annotation(annotation: Annotations, user_id: UUID) -> None:
    query = """INSERT INTO "annotations"(date, description, user_id) VALUES (%(date)s, %(description)s, %(user_id)s);"""
    user_id = str(user_id)

    parameters = {
        'date': annotation.date,
        'description': annotation.description,
        'user_id': user_id,
    }
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
            conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()