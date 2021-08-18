import pytz
from django.utils.timezone import make_aware
from ics import Calendar, Event
from datetime import datetime, time, timedelta
from rest_framework import serializers
from event.models import UserEvent, PublicHoliday


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ('name', 'start_date', 'end_date', 'reminder_before', )

    def create(self, validated_data):
        reminder_before = validated_data.get('reminder_before')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        user = self.context.get('request').user
        validated_data['user'] = user
        user_email = self.context.get('request').user.email
        if end_date is None:
            validated_data['end_date'] = make_aware(datetime.combine(start_date, time.max))
        return super().create(validated_data)


class EventsOfDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserEvent
        fields = ('name', 'start_date')


class EveryDayEventsOfMonthSerializer(serializers.Serializer):
        date = serializers.DateField()
        events = EventsOfDaySerializer(many=True)


class GetEventsFromICSSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=124)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()


class PublicHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ('name', 'start_date')

