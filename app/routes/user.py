from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.common.database import contact_collection
from app.auth.dependencies import user_dependency
from app.common.schemas.user_schema import UserCreate, UserOut, Contact
from app.auth.auth_handlers import create_user, login_for_access_token

router = APIRouter()


@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    return await create_user(user)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token(form_data)


@router.get("/me")
async def read_users_me(current_user: user_dependency):
    return current_user

@router.post("/contact")
async def contact(details: Contact, current_user: user_dependency):
    details = details.model_dump()
    details["user_id"] = str(current_user.id)
    await contact_collection.insert_one(details)
    details.pop("_id")
    return details