from django.conf.urls import url
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from authentication.views import UserCreateAPIView, UserProfileUpdateAPIView, UserActivationView

urlpatterns = [
    path('registration/', UserCreateAPIView.as_view()),
    path('profile_edit/', UserProfileUpdateAPIView.as_view()),
    url(r'^activation/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='login'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
