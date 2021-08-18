from django.core.mail import send_mail
from ics import Calendar
import requests
from event.models import PublicHoliday, Country
from rest_framework.response import Response
from rest_framework import status


def send(user_email):
    send_mail(
        'событие',
        'ваше событие начнется',
        'forallneedz@gmail.com',
        [user_email],
        fail_silently=False
    )


def import_from_ics(country):
    """Извлечение государственных праздников из файла формата ics и сохранение в базу"""
    url = "https://www.officeholidays.com/ics/ics_country.php?tbl_country=" + country
    all_publish_event = Calendar(requests.get(url).text)
    for event in all_publish_event.events:
        publish_event = PublicHoliday()
        publish_event.country = Country.objects.get(name=country)
        publish_event.name = event.name
        publish_event.start_date = event._begin.datetime
        publish_event.end_date = event._end_time.datetime
        publish_event.save()
    return Response(status=status.HTTP_201_CREATED)
