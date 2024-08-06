import re
from fastapi import HTTPException
from psycopg2 import IntegrityError

from api.services.db import connect
from api.models.AnnotationsModels import AnnotationsIn


async def create_annotation(annotation: AnnotationsIn) -> None:
    query = """INSERT INTO "annotations"(date, description, user_id) VALUES (%(date)s, %(description)s, %(user_id)s);"""
    annotation.user_id = str(annotation.user_id)

    parameters = {
        'date': annotation.date,
        'description': annotation.description,
        'user_id': annotation.user_id,
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