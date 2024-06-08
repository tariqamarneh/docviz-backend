from bson import ObjectId
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.common.models.users import User
from app.auth.jwt import decode_access_token
from app.common.database import user_collection
from app.common.logging.logger import mongo_logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


async def get_user_by_id(user_id: str):
    return await user_collection.find_one({"_id": ObjectId(user_id)})


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        # mongo_logger.error("Could not validate credentials")
        raise credentials_exception
    user = await get_user_by_id(payload.get("sub"))
    if user is None:
        # mongo_logger.error("Could not validate credentials")
        raise credentials_exception
    return User(id=str(user["_id"]), **user)


user_dependency = Annotated[User, Depends(get_current_user)]
