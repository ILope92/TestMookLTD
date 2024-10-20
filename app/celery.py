from celery import Celery
from celery.schedules import crontab

from app.core.base.celery import get_celery_app

app: Celery = get_celery_app()
app.autodiscover_tasks(["app.celery.tasks"])
app.conf.timezone = "UTC"
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    "add-every-monday-morning": {
        "task": "app.applications.pages.tasks.get_btc_price",
        "schedule": float((60 * 60) * 3),
    },
    "exhanges_task": {
        "task": "closed_exchanges",
        "schedule": float(60),
    },
}


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.send_task("get_btc_price")
    # sender.send_task("closed_exchanges")
    pass
