from django.urls import path

from event import views

urlpatterns = [
    path("create_event/", views.UserEventListCreateAPIView.as_view(), name="create_event"),
    path("pars_event/", views.GetEventsFromICS.as_view(), name="pars_event"),
    path("get_user_event/<int:user_id>/<int:month>/<int:year>", views.SortedEventsByMonthAPIView.as_view(), name="get_user_event"),

]