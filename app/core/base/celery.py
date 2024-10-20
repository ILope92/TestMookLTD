from celery import Celery
from app.core.loader import settings


def get_celery_app() -> Celery:
    app = Celery(
        "tasks",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )

    return app
