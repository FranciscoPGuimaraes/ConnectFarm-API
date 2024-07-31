from typing import List
from fastapi import HTTPException
from datetime import datetime

from api.services.db import connect
from api.models.AnnotationsModels import Annotations

async def get_annotations_by_userid(user_id: str) -> List[Annotations]:
    query = """
            SELECT id, user_id, date, description
            FROM "annotations"
            WHERE user_id = %(user_id)s;
            """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"user_id": user_id})
                result = cursor.fetchall()

                if result:
                    annotations = [
                        Annotations(
                            id=row[0], 
                            user_id=row[1], 
                            date=row[2].strftime('%Y-%m-%d'),
                            description=row[3]
                        ) 
                        for row in result
                    ]
                    return annotations
                else:
                    return []

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
