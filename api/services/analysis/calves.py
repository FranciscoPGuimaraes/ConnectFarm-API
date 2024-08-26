from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo
from datetime import datetime


async def calculate_weaned_calves_ratio(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    
    try:
        farm_id = str(farm_id)
        
        total_cows = collection.count_documents({"farm_id": farm_id})
        
        pipeline = [
            {"$match": {"farm_id": farm_id}},
            {"$unwind": "$calves"},
            {"$match": {"calves.weaning": {"$exists": True}}}
        ]
        weaned_calves_count = collection.aggregate(pipeline)
        weaned_calves_count = sum(1 for _ in weaned_calves_count)

        if total_cows == 0:
            return {"message": "No cows found in the specified farm_id."}
        
        weaned_ratio = weaned_calves_count / total_cows
        return {
            "total_cows": total_cows,
            "weaned_calves": weaned_calves_count,
            "weaned_ratio": weaned_ratio
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating weaned calves ratio: {e}")
    
    
async def analyze_weaning_time(farm_id: UUID):
    collection, client = connect_mongo("cattles")
    
    try:
        farm_id = str(farm_id)
        weaning_times = []
        
        # Consulta para obter todos os bezerros de uma fazenda específica
        pipeline = [
            {"$match": {"farm_id": farm_id}},  # Filtrar vacas pela fazenda
            {"$unwind": "$calves"},            # Desagregar a lista de bezerros
            {"$match": {"calves.weaning": {"$exists": True}}}  # Filtrar bezerros com 'weaning' preenchido
        ]
        cursor = collection.aggregate(pipeline)
        
        for cattle in cursor:
            calf = cattle.get("calves")
            birth_date_str = calf.get("birth_date")
            weaning_date_str = calf.get("weaning")
            
            if birth_date_str and weaning_date_str:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
                weaning_date = datetime.strptime(weaning_date_str, "%Y-%m-%d")
                weaning_time = (weaning_date - birth_date).days
                weaning_times.append(weaning_time)
        
        # Cálculo das métricas de desmame
        if weaning_times:
            average_weaning_time = sum(weaning_times) / len(weaning_times)
            min_weaning_time = min(weaning_times)
            max_weaning_time = max(weaning_times)
        else:
            average_weaning_time = min_weaning_time = max_weaning_time = None
        
        result = {
            "total_calves_weaned": len(weaning_times),
            "average_weaning_time": average_weaning_time,
            "min_weaning_time": min_weaning_time,
            "max_weaning_time": max_weaning_time,
        }
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing weaning time: {e}")