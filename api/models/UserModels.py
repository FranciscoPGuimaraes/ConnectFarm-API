from typing import Optional

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    name: str = Field(max_length=150)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=15)  
    birth: str = Field(max_length=10)  


class UserIn(UserOut):
    cpf: str = Field(max_length=14)
    password: str = Field(max_length=64)


class UserInDB(BaseModel):
    hashed_password: str
    user_id: str
    

class UserInQuery(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    email: Optional[str] = Field(None, max_length=100)  
    phone: Optional[str] = Field(None, max_length=15)  
    birth: Optional[str] = Field(None, max_length=10)  
