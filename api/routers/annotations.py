from typing import Dict, List
from fastapi import APIRouter

from api.models.AnnotationsModels import Annotations, AnnotationsIn
from api.services.annotations import create_annotation, get_annotations_by_userid

router = APIRouter(
    prefix="/annotations",
    tags=["Annotations"],
)

@router.post("/create", response_model=Dict)
async def create_annotation_endpoint(annotation: AnnotationsIn):
    try:
        await create_annotation(annotation)
    except Exception as err:
        return {"message": f"Erro ao criar anotação: {err}"}
    else:
        return {"message": f"Annotation created successfully!"}

@router.get("/{user_id}", response_model=List[Annotations])
async def get_annotations_by_userid_endpoint(user_id: str):
    return await get_annotations_by_userid(user_id)
