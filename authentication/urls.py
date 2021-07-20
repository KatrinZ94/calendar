from django.conf.urls import url
from django.urls import path, include

from authentication.views import UserCreateAPIView, UserProfileUpdateAPIView, UserActivationView

urlpatterns = [
    path('registration/', UserCreateAPIView.as_view()),
    path('profile_edit/<int:profile_id>', UserProfileUpdateAPIView.as_view()),
    url(r'^activation/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),

]
