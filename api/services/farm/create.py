from uuid import UUID
from fastapi import HTTPException

from api.models.FarmModels import FarmIn
from api.services.db import connect


async def create_farm(farm: FarmIn, owner_id: UUID) -> None:
    base_query = "INSERT INTO farm(owner_id, name, address"
    base_values = "VALUES (%(owner_id)s, %(name)s, %(address)s"
    parameters = {
        "owner_id": owner_id,
        "name": farm.name,
        "address": farm.address,
    }

    if farm.area:
        base_query += ", area"
        base_values += ", %(area)s"
        parameters["area"] = farm.area

    if farm.objective:
        base_query += ", objective"
        base_values += ", %(objective)s"
        parameters["objective"] = farm.objective

    query = base_query + ") " + base_values + ");"
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
