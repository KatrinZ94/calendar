from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView
from event.models import UserEvent
from event.serializer import UserEventSerializer


class UserEventListCreateAPIView(ListCreateAPIView):
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer

