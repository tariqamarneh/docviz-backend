from datetime import timedelta

from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.jwt import create_access_token
from app.common.models.users import UserInDB
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.common.logging.logger import mongo_logger
from app.common.schemas.user_schema import UserCreate, Token
from app.common.database import user_collection, password_collection


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if user is None:
        return False
    password_data = await password_collection.find_one({"user_id": user["_id"]})
    if password_data is None:
        return False
    if not verify_password(password, password_data["hashed_password"]):
        return False
    return UserInDB(
        id=str(user["_id"]), **user, hashed_password=password_data["hashed_password"]
    )


async def create_user(user: UserCreate):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        mongo_logger.warning("Email already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    user_data = await user_collection.insert_one(
        {"email": user.email, "full_name": user.full_name}
    )
    await password_collection.insert_one(
        {"user_id": user_data.inserted_id, "hashed_password": hashed_password}
    )
    return user


async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        mongo_logger.warning("Incorrect email or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
