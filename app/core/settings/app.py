from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str
    API_PREFIX: str = "/api/v1"
