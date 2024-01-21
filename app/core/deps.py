from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import User
from app.schemas.token import TokenData
from jose import JWTError, jwt

from app.services.user import UserService
from app.core.config import get_app_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/login")

settings = get_app_settings()

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends()
    ) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = user_service.get_by_username(username=token_data.username)
    
    if user is None:
        raise credentials_exception
    
    return user
