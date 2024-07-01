from typing import Optional

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    name: str = Field(max_length=50)
    email: str = Field(max_length=30)
    phone: str = Field(None, max_length=11)  
    birth: str = Field(max_length=10)  


class UserIn(UserOut):
    cpf: str = Field(max_length=11)
    password: str = Field(max_length=64)

class UserInDB(UserOut):
    hashed_password: str
    

class UserInQuery(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=30)  
    phone: Optional[str] = Field(None, max_length=30)  
    birth: Optional[str] = Field(None, max_length=30)  