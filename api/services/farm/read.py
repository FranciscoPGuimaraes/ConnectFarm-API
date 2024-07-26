from typing import List
from uuid import UUID
from fastapi import HTTPException
from api.models.FarmModels import FarmOut
from api.services.db import connect

async def read_farm(farm_id: UUID) -> FarmOut:
    query = """
            SELECT f.name, f.address, f.farm_id
            FROM farm f
            WHERE f.farm_id = %(farm_id)s;
            """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"farm_id": farm_id})
                result = cursor.fetchone()

                if result:
                    farm: FarmOut
                    farm = FarmOut(
                        name=result[0],
                        address=result[1],
                        farm_id=result[2]
                    )

                    return farm
                else:
                    return None
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()
        
        
async def read_farms_from_user(user_id: UUID) -> List[FarmOut]:
    query = """
            SELECT f.name, f.address, f.farm_id
            FROM farm f
            WHERE f.owner_id = %(owner_id)s;
            """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"owner_id": user_id})
                results = cursor.fetchall()
                
                if results:
                    farms: List[FarmOut] = []
                    for result in results:
                        farms.append(FarmOut(
                            name=result[0],
                            address=result[1],
                            farm_id=result[2]
                        ))
                    return farms
                else:
                    return None
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()