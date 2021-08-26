from django.core.mail import send_mail

from daily.celery import app
from event.constants import countries
from event.models import UserEvent

from .service import send, import_from_ics


@app.task
def send_reminder_email(user_email, event_id, start_date, event_name):
    send(user_email, event_name, start_date)


@app.task
def refresh_public_holiday():
    for country in countries:
        import_from_ics(country)

