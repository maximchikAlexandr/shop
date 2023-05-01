from shop_project.celery import app
from catalog.services import EmailSender


@app.task
def send_newsletters():
    EmailSender().send_newsletter()
