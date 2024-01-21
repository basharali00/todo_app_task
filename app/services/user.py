from typing import Optional
from datetime import timedelta

from fastapi import Depends, HTTPException, status
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.security import verify_password, create_access_token, get_password_hash
from app.repositories.users import UsersRepository, get_users_repository
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.core.config import get_app_settings

settings = get_app_settings()

class UserService:
    def __init__(
        self, user_repo: UsersRepository = Depends(get_users_repository)
    ) -> None:
        self.user_repo = user_repo

    def login(self, user: UserLogin) -> Token:
        self.authenticate(username=user.username, password=user.password)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

        return Token(
            access_token=access_token,
            token_type="bearer"
        )

    def register(self, user_create: UserCreate) -> User:
        db_user = self.user_repo.get_by_username(username=user_create.username)
        if db_user:
            raise HTTPException(status_code=400, detail="username already registered")
        user_create.password = get_password_hash(password=user_create.password)
        user = self.user_repo.create(obj_create=user_create)
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        return self.user_repo.get_by_username(username=username)

    def authenticate(self, username: str, password: str) -> User:
        user = self.user_repo.get_by_username(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(
            plain_password=password, hashed_password=user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user