from daily.celery import app

from .service import send, import_from_ics


@app.task
def send_reminder_email(user_email):
    send(user_email)


@app.task
def refresh_public_holiday(country_name):
    import_from_ics(country_name)
