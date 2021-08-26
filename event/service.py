from django.core.mail import send_mail
from ics import Calendar
import requests
from event.models import PublicHoliday, Country
import uuid
from datetime import datetime


def send(user_email, event_name, start_date):
    send_mail(
        f'напоминание о событии "{event_name}"',
        f'Ваше событие "{event_name}" начнется в {datetime.fromisoformat(start_date)}',
        'forallneedz@gmail.com',
        [user_email],
        fail_silently=False
    )


def import_from_ics(country_name):
    """Извлечение государственных праздников из файла формата ics и сохранение в базу"""
    try:
        country_id_on_deleted = Country.objects.get(name=country_name).id
        PublicHoliday.objects.filter(country_id=country_id_on_deleted).delete()
        url = "https://www.officeholidays.com/ics/ics_country.php?tbl_country=" + country_name
        all_publish_event = Calendar(requests.get(url).text)
        for event in all_publish_event.events:
            publish_event = PublicHoliday()
            publish_event.country = Country.objects.get(name=country_name)
            publish_event.name = event.name
            publish_event.start_date = event._begin.datetime
            publish_event.end_date = event._end_time.datetime
            publish_event.save()
    except:
        pass

#
# def get_uuid(event_id):
#     task_id = str(uuid.UUID(int=event_id))
#     return task_id
