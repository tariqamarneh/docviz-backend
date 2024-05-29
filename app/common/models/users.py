from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    full_name: str


class UserInDB(User):
    hashed_password: str
