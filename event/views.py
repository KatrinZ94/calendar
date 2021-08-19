import pytz
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from rest_framework import status, filters, pagination

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ics import Calendar
import calendar
import requests
from datetime import datetime, timedelta, timezone
from event.models import UserEvent, PublicHoliday, Country
from event.serializer import UserEventSerializer, EventsOfDaySerializer, EveryDayEventsOfMonthSerializer, \
    PublicHolidaySerializer
from event.service import send
from event.tasks import send_reminder_email


class PaginatorAllEvents(pagination.LimitOffsetPagination):
    max_limit = 5


# ПОЛЬЗОВАТЕЛЬСКИЕ СОБЫТИЯ
class UserEventCreateAPIView(CreateAPIView):
    """Создание пользовательского события"""
    permission_classes = [IsAuthenticated]
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        reminder_before = request.data.get('reminder_before')
        start_date = request.data['start_date']
        user_email = request.user.email
        if reminder_before is not None:
            start_date = datetime.fromisoformat(start_date)
            date_to_reminder = start_date - timedelta(hours=reminder_before)
            event_name = request.data['name']
            send_reminder_email.apply_async(args=(user_email, event_name, start_date), eta=date_to_reminder)
        return response


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
    serializer_class = UserEventSerializer

    def get_queryset(self):
        queryset = UserEvent.objects.filter(user_id=self.request.user.id)
        return queryset


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
    """"Вывод всех событий потзователя по дням за определенный месяц года (агрегация)"""
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
# class GetEventsFromICS(APIView):
#     """Извлечение государственных праздников из файла формата ics и сохранение в базу"""
#
#     def post(self, request, *args, **kwargs):
#         country_from_request = request.META.get('HTTP_COUNTRY_NAME')
#         country_id_on_deleted = Country.objects.get(name=country_from_request).id
#         PublicHoliday.objects.filter(country_id=country_id_on_deleted).delete()
#
#         url = "https://www.officeholidays.com/ics/ics_country.php?tbl_country="+country_from_request
#         all_publish_event = Calendar(requests.get(url).text)
#         for event in all_publish_event.events:
#             publish_event = PublicHoliday()
#             publish_event.country = Country.objects.get(name=country_from_request)
#             publish_event.name = event.name
#             publish_event.start_date = event._begin.datetime
#             publish_event.end_date = event._end_time.datetime
#             publish_event.save()
#         return Response(status=status.HTTP_201_CREATED)


class PublicHolidayAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, month, year):
        country_id = request.user.profile.country_id
        events_of_month = PublicHoliday.objects.filter(country_id=country_id, start_date__year=year, start_date__month=month)
        serializer = PublicHolidaySerializer(events_of_month, many=True)
        return Response(serializer.data)


class SendEmail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email
        send(email)
        return Response()


# class CeleryPublicHoliday():
#     def choose_the_country(self):
#         countries = Country.objects.all()
#         for country in countries:
#             url ="pars_event/"+