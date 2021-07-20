from rest_framework import status, filters, pagination

from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ics import Calendar
import requests
from datetime import datetime
from event.models import UserEvent, PublicHoliday, Country
from event.serializer import UserEventSerializer, GetEventsFromICSSerializer, SortedEventsSerializer


class PaginatorAllEvents(pagination.LimitOffsetPagination):
    max_limit = 5


class UserEventListCreateAPIView(CreateAPIView):
    '''Создание пользовательского события'''
    permission_classes = [IsAuthenticated]
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ['start_date', ]
    pagination_class = PaginatorAllEvents


class UserEventEditingAPIView(RetrieveUpdateDestroyAPIView):
    """Редактирование пользовательского события"""
    queryset = UserEvent.objects.get
    serializer_class = UserEventSerializer
    permission_classes = [IsAuthenticated]


class GetEventsFromICS(APIView):
    """Извлечение государственных праздников из файла формата ics и сохранение в базу"""

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
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, month, year):
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1)
        events = UserEvent.objects.filter(user_id=user_id, start_date__range=(start_date, end_date))
        serializer = UserEventSerializer(events, many=True)
        return Response(serializer.data)
