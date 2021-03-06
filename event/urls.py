from django.urls import path

from event import views

urlpatterns = [
    path("create_event/", views.UserEventCreateAPIView.as_view(), name="create_event"),
    path("event/<int:id_event>", views.UserEventEditingAPIView.as_view(), name="event"),
    path("all_events/", views.AllUserEventAPIView.as_view(), name="all_events"),
    path("events_of_day/<int:day>/<int:month>/<int:year>", views.EventsOfDay.as_view(), name="events_of_day"),
    path("events_of_month/<int:month>/<int:year>", views.EveryDayEventsOfMonth.as_view(), name="events_of_month"),
    path("public_holiday/<int:month>/<int:year>", views.PublicHolidayAPIView.as_view(), name="public_holiday"),

]