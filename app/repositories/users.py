from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import get_app_settings
from .base import BaseRepository
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

settings = get_app_settings()

class UsersRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()


def get_users_repository(session: Session = Depends(get_db)) -> UsersRepository:
    return UsersRepository(db=session, model=User)
