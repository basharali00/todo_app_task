from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.deps import get_current_user
from app.schemas.user import UserCreate, User, UserLogin
from app.schemas.token import Token
from app.services.user import UserService

router = APIRouter()

@router.get("/me", response_model=User)
def get_user(user: User = Depends(get_current_user)) -> User:
    return user

@router.post("", response_model=User)
def register_user(
    user: UserCreate,
    user_service: UserService = Depends()
) -> User:
    user = user_service.register(user_create=user)
    return user

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends()
) -> Token:
    return user_service.login(
        user = UserLogin(
            username=form_data.username,
            password=form_data.password
        )
    )

