import os
from dotenv import load_dotenv

load_dotenv(".env")

class Settings:
    VERSION: str = "0.0.1a"
    APP_TITLE: str = "Test Mook LTD"
    PROJECT_NAME: str = "Test Mook LTD"

    PROJECT_ROOT: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir),
    )
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    TEMPLATES_PATH: str = os.path.join(BASE_DIR, "./frontend/templates")
    PATH_LOG_DATA: str = "app/logs"

    # Time live tokens
    TOKEN_IN_COOKIES_NAME: str = "XSRF-TOKEN"
    TOKEN_LOGIN_NAME: str = "token_login"
    TOKEN_LOGIN_TIME: int = 660

    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND")

    # DATABASE
    POSTGRES_DATABASE_URL: str = "postgresql+asyncpg://admin:admin@postgres:5432/postgresdb"  # os.getenv("DATABASE_URL")
    # Auth data
    AUTH_SECRET_KEY: str = ""
    AUTH_ALGORITHM: str = ""


settings = Settings()

