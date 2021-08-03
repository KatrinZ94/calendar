from daily.celery import app

from .service import send


@app.task
def send_reminder_email(user_email):
    send(user_email)
