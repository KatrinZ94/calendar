from django.core.mail import send_mail

from daily.celery import app
from event.constants import countries

from .service import send, import_from_ics


@app.task
def send_reminder_email(user_email, event_name, start_date):
    send(user_email, event_name, start_date)


@app.task
def refresh_public_holiday():
    for country in countries:
        import_from_ics(country)

