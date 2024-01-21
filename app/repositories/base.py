from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, db: Session, model: Type[ModelType]) -> None:
        self.db = db
        self.model = model

    def get_all(self) -> List[ModelType]:
        return self.db.query(self.model).all()

    def get(self, obj_id: str) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def create(self, obj_create: CreateSchemaType) -> ModelType:
        obj = self.model(**obj_create.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj_id: str) -> Optional[ModelType]:
        obj = self.db.query(self.model).get(obj_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return obj