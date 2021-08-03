from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, get_object_or_404
from django.contrib.auth.models import User
from authentication.models import UserProfile
from authentication.serializers import UserSerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework.permissions import IsAuthenticated

class UserActivationView(APIView):
    """Активация юзера по ссылке"""
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        content = result.text
        return Response(content)


class UserCreateAPIView(CreateAPIView):
    """"Регистрация/создание профиля + отправка email"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    """"Редактирование профиля"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        profile_id = self.request.user.profile.id
        return get_object_or_404(UserProfile, id=profile_id)

