from rest_framework import status, filters, pagination

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ics import Calendar
import calendar
import requests
from datetime import datetime, timedelta
from event.models import UserEvent, PublicHoliday, Country
from event.serializer import UserEventSerializer, EventsOfDaySerializer, EveryDayEventsOfMonthSerializer


class PaginatorAllEvents(pagination.LimitOffsetPagination):
    max_limit = 5


# ПОЛЬЗОВАТЕЛЬСКИЕ СОБЫТИЯ
class UserEventCreateAPIView(CreateAPIView):
    """Создание пользовательского события"""
    permission_classes = [IsAuthenticated]
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer
    # filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    # search_fields = ('name',)
    # ordering_fields = ['start_date', ]
    # pagination_class = PaginatorAllEvents


class UserEventEditingAPIView(RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование и удаление пользовательского события"""
    serializer_class = UserEventSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_id = self.kwargs.get('id_event')
        user_id = self.request.user.id
        return get_object_or_404(UserEvent, id=event_id, user_id=user_id)


class AllUserEventAPIView(ListAPIView):
    """Все пользовательские события"""
    permission_classes = [IsAuthenticated]
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer

class EventsOfDay(APIView):
    """Вывод всех событий пользователя за определенный день"""
    permission_classes = [IsAuthenticated]

    def get(self, request, day, month, year):
        user_id = request.user.id
        date = datetime(year, month, day).date()
        events = UserEvent.objects.filter(user_id=user_id, start_date__date=date)
        serializer = EventsOfDaySerializer(events, many=True)
        return Response(serializer.data)


class EventDate:
    def __init__(self, date, events):
        self.date = date
        self.events = events


class EveryDayEventsOfMonth(APIView):
    """"Вывод всех событий потзователя по дням за определенный месяц года"""
    permission_classes = [IsAuthenticated]

    def get(self, request, month, year):
        user_id = request.user.id
        count_day = calendar.monthrange(year, month)[1]
        events_of_month = UserEvent.objects.filter(user_id=user_id, start_date__year=year, start_date__month=month)
        aggregated_events = []
        for day in range(1, count_day + 1):
            every_day = datetime(year, month, day).date()
            events = [event for event in events_of_month if event.start_date.date() == every_day]
            events_date = EventDate(every_day, events)
            aggregated_events.append(events_date)
        serializer = EveryDayEventsOfMonthSerializer(aggregated_events, many=True)
        return Response(serializer.data)


# ГОСУДАРСТВЕННЫЕ ПРАЗДНИКИ
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
