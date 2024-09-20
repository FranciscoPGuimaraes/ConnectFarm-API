from typing import Dict, List
from fastapi import APIRouter, Depends, Security

from api.dependencies import get_api_key, get_current_user, get_current_user_id
from api.models.AnnotationsModels import Annotations
from api.services.annotations import create_annotation, get_annotations_by_userid

router = APIRouter(
    prefix="/annotations",
    tags=["Annotations"],
    dependencies=[Depends(get_api_key), Security(get_current_user)]
)

@router.post("/create", response_model=Dict)
async def create_annotation_endpoint(annotation: Annotations, current_user_id: Dict = Depends(get_current_user_id)):
    try:
        await create_annotation(annotation, current_user_id)
    except Exception as err:
        return {"message": f"Erro ao criar anotação: {err}"}
    else:
        return {"message": f"Annotation created successfully!"}

@router.get("/", response_model=List[Annotations])
async def get_annotations_by_userid_endpoint(current_user_id: Dict = Depends(get_current_user_id)):
    return await get_annotations_by_userid(current_user_id)
