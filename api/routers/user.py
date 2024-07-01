from typing import Optional, List, Dict

from fastapi import APIRouter, Security, Depends, HTTPException, Query

#from api.dependencies import get_current_user, get_password_hash, get_api_key
from api.internal.user import create_user, get_all_users
from api.models.UserModels import UserOut, UserInQuery, Userin

router = APIRouter(
    prefix="/user",
    tags=["User"]
    #dependencies=[Security(get_current_user, scopes=[UserScope.admin.value]), Depends(get_api_key)]
)

@router.post("/create", response_model=Dict)
async def create_new_user(user: Userin) -> Dict:
    try:
        await create_user(user)
        return {"message": f"User with name {user.name} created successfully!"}
    except Exception as e:
        raise e

@router.get("/", response_model=Dict)
async def get_all() -> Optional[List[UserOut]]:
    try:
        users = await get_all_users()
        return users
    except Exception as e:
        raise e
    

    