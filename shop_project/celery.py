import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_project.settings")

app = Celery("shop_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "every": {
        "task": "catalog.tasks.send_newsletters",
        "schedule": crontab(minute="48", hour="19", day_of_week="mon"),
    },
}
