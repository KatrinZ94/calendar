
from django.shortcuts import render


# Create your views here.
from pip._vendor import requests
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from ics import Calendar

from event.models import UserEvent, GarmentEvent
from event.serializer import UserEventSerializer, GetEventsFromICSSerializer


class UserEventListCreateAPIView(ListCreateAPIView):
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer


class GetEventsFromICS(ListAPIView):
    serializer_class = GetEventsFromICSSerializer
    url = "https://www.officeholidays.com/ics/ics_country.php?tbl_country=russia"
    c = Calendar(requests.get(url).text)
    gov_arr = []
    for gav_event in c.events:
        gov_arr.append(GarmentEvent(gav_event.name, gav_event._begin, gav_event._end_time))

    queryset = gov_arr



    # def get(self, request, *args, **kwargs):
    #     serializer_class=GetEventsFromICSSerializer
    #     queryset = myarr
    #     url = "https://urlab.be/events/urlab.ics"
    #     c = Calendar(requests.get(url).text)
    #     c.events
    #     e = list(c.timeline)
    #     myarr = []
    #     for i in e:
    #         arr_elem = ("Event '{}' started {}".format(i.name, i.begin.humanize()))
    #         myarr.append(arr_elem)
    #     return self.list(request, *args, **kwargs)
