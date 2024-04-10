from fastapi import APIRouter

router = APIRouter()

@router.get("/culture/")
async def read_culture():
    return [{"username": "Foo"}, {"username": "Bar"}]