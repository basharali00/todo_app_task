from fastapi import APIRouter

from app.api.v1.routes import user, task

router = APIRouter()

router.include_router(router=user.router, tags=["Users"], prefix="/user")
router.include_router(router=task.router, tags=["Tasks"], prefix="/task")