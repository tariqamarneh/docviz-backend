from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.dependencies import get_current_user
from app.auth.auth_handlers import create_user, login_for_access_token
from app.common.schemas.user_schema import UserCreate, UserOut

router = APIRouter()


@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    return await create_user(user)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token(form_data)


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
