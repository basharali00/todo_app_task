from sqlalchemy import Column, ForeignKey, String, Boolean, text
from app.db.session import Base


class UserShareTask(Base):
    __tablename__ = "users_share_tasks"

    id = Column(String, primary_key=True, default=text("gen_random_uuid()"))
    owner_id = Column(String, ForeignKey("users.id"))
    share_to_id = Column(String, ForeignKey("users.id"))
    task_id = Column(String, ForeignKey("tasks.id"))
    is_enabled = Column(Boolean, default=True)