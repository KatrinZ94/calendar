from djoser import signals
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from authentication.models import UserProfile
from djoser.conf import settings


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'profile')
        unique_together = ('email',)
        extra_kwargs = {'email': {'required': True, 'allow_blank': False, 'validators': [
                        UniqueValidator(
                            queryset=User.objects.all()
                        )
                    ]}}

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile)
        if settings.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            user.save(update_fields=["is_active"])
        return user

