from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    full_name: str


class UserInDB(User):
    hashed_password: str
