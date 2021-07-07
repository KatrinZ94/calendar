from django.urls import path

from event import views

urlpatterns = [
    path("user_event/", views.UserEventListCreateAPIView.as_view(), name="create_event"),

]