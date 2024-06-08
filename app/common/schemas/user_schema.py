import re
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from app.common.logging.logger import mongo_logger


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

    @field_validator("email")
    def email_must_be_valid(cls, v):
        if not re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", v):
            mongo_logger.warning("The email must be valid")
            raise HTTPException(detail="The Email Must Be Valid", status_code=400)
        return v


class UserOut(BaseModel):
    email: EmailStr
    full_name: str


class Token(BaseModel):
    access_token: str
    token_type: str

class Contact(BaseModel):
    name: str
    email: EmailStr
    message: str

    @field_validator("email")
    def email_must_be_valid(cls, v):
        if not re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", v):
            mongo_logger.warning("The email must be valid")
            raise HTTPException(detail="The Email Must Be Valid", status_code=400)
        return v
