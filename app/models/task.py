from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from app.db.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=text("gen_random_uuid()"))
    title = Column(String, index=True)
    status = Column(Boolean, default=False)
    order = Column(Integer)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")