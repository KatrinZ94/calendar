#from django.contrib.sites import requests
from django.shortcuts import render
# Create your views here.
#from pip._vendor import requests
from ics import Calendar
from rest_framework import status

from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from ics import Calendar
import requests
from datetime import datetime
from event.models import UserEvent, PublicHoliday, Country
from event.serializer import UserEventSerializer, GetEventsFromICSSerializer, SortedEventsSerializer


class UserEventListCreateAPIView(ListCreateAPIView):
    '''Создание пользовательского события'''
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer


class GetEventsFromICS(APIView):
    """Извлечение государственных праздников из файла формата ics и сохранение в базу"""
    # serializer_class = GetEventsFromICSSerializer
    # url = "https://www.officeholidays.com/ics/ics_country.php?tbl_country=russia"
    # c = Calendar(requests.get(url).text)
    # gov_arr = []
    # for gav_event in c.events:
    #     gov_arr.append(PublicHoliday(gav_event.name, gav_event._begin, gav_event._end_time))
    # queryset = gov_arr

    def post(self, request, *args, **kwargs):
        country_from_request = request.META.get('HTTP_COUNTRY_NAME')
        country_id_on_deleted = Country.objects.get(name=country_from_request).id
        PublicHoliday.objects.filter(country_id=country_id_on_deleted).delete()

        url = "https://www.officeholidays.com/ics/ics_country.php?tbl_country="+country_from_request
        all_publish_event = Calendar(requests.get(url).text)
        for event in all_publish_event.events:
            publish_event = PublicHoliday()
            publish_event.country = Country.objects.get(name=country_from_request)
            publish_event.name = event.name
            publish_event.start_date = event._begin.datetime
            publish_event.end_date = event._end_time.datetime
            publish_event.save()
        return Response(status=status.HTTP_201_CREATED)


class SortedEventsByMonthAPIView(APIView):
    """вывод всех событий определенного пользователя за заданный месяц года"""
    def get(self, request, user_id, month, year):
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1)
        events = UserEvent.objects.filter(user_id=user_id, start_date__range=(start_date, end_date))
        serializer = UserEventSerializer(events, many=True)
        return Response(serializer.data)
