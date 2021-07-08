from ics import Calendar, Event
from datetime import datetime, time

from rest_framework import serializers

from event.models import UserEvent, GarmentEvent


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = '__all__'

    def create(self, validated_data):
        end_date = validated_data.get('end_date')
        if end_date is None:
            start_date = validated_data.get('start_date')
            validated_data['end_date'] = datetime.combine(start_date, time.max)
        return super().create(validated_data)


class GetEventsFromICSSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=124)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
