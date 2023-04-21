import time
from celery import shared_task


@shared_task
def some_task():
    time.sleep(10)
    return 'aboba'


@shared_task
def scheduled_task():
    return 'susiubake'
