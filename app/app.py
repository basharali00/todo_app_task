from fastapi import FastAPI

from app.models import task, user, user_share_tasks
from app.api.v1.router import router as api_router
from app.db.session import engine
from app.core.config import get_app_settings

def create_app() -> FastAPI:
    user.Base.metadata.create_all(bind=engine)
    task.Base.metadata.create_all(bind=engine)
    user_share_tasks.Base.metadata.create_all(bind=engine)

    settings = get_app_settings()

    application = FastAPI()

    application.include_router(api_router, prefix=settings.API_PREFIX)

    return application


app = create_app()