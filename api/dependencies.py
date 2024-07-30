import os
from datetime import timedelta, datetime, timezone
from typing import Union, Annotated
import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette.status import HTTP_403_FORBIDDEN

from dotenv import load_dotenv

from api.models.UserModels import UserInDB

from .models.structural.TokenModels import TokenData
from .services.user import get_user_by_email_for_auth


load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


async def get_api_key(X_API_Key: str = Security(api_key_header)):
    if X_API_Key == os.getenv("API_KEY"):
        return X_API_Key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str):
    user: UserInDB = await get_user_by_email_for_auth(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=600)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email_for_auth(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except InvalidTokenError:
        raise Exception
