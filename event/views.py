from celery.worker.control import revoke
from rest_framework import pagination
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import calendar
from datetime import datetime, timedelta
from daily.celery import app
from event.models import UserEvent, PublicHoliday, Task
from event.serializer import UserEventSerializer, EventsOfDaySerializer, EveryDayEventsOfMonthSerializer, \
    PublicHolidaySerializer
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
        event_name = request.data['name']
        if reminder_before is not None:
            start_date_in_UTC = datetime.fromisoformat(start_date)
            date_to_reminder = start_date_in_UTC - timedelta(hours=reminder_before)
            event_id = response.data['id']
            task = Task.objects.create(event_id=event_id)
            send_reminder_email.apply_async(args=(user_email, event_id, start_date, event_name), task_id=str(task.id), eta=date_to_reminder)
        return response


class UserEventEditingAPIView(RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование и удаление пользовательского события"""
    serializer_class = UserEventSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_id = self.kwargs.get('id_event')
        user_id = self.request.user.id
        return get_object_or_404(UserEvent, id=event_id, user_id=user_id)

    def perform_update(self, serializer):
        serializer.save()
        reminder_before = self.request.data.get('reminder_before')
        start_date = self.request.data['start_date']
        event_name = self.request.data['name']
        user_email = self.request.user.email
        event_id = self.kwargs['id_event']
        task = Task.objects.filter(event_id=event_id).first()
        if task is not None:
            app.control.revoke(str(task.id), terminate=True)
            task.delete()
        if reminder_before is not None:
            start_date_in_UTC = datetime.fromisoformat(start_date)
            date_to_reminder = start_date_in_UTC - timedelta(hours=reminder_before)
            task = Task.objects.create(event_id=event_id)
            send_reminder_email.apply_async(args=(user_email, event_id, start_date, event_name), task_id=str(task.id),
                                            eta=date_to_reminder, state='RECEIVED')

    def perform_destroy(self, instance):
        event_id = self.kwargs['id_event']
        task = Task.objects.get(event_id=event_id)
        app.control.revoke(str(task.id), terminate=True)
        instance.delete()


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

class PublicHolidayAPIView(APIView):
    """Государственные праздники за выбранный месяц"""
    permission_classes = [IsAuthenticated]

    def get(self, request, month, year):
        country_id = request.user.profile.country_id
        events_of_month = PublicHoliday.objects.filter(country_id=country_id, start_date__year=year, start_date__month=month)
        serializer = PublicHolidaySerializer(events_of_month, many=True)
        return Response(serializer.data)

