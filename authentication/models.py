from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from event.models import Country
from datetime import datetime


def upload_to(instance, filename):
    date = datetime.now().strftime("%Y/%m/%d")
    return f"{instance.first_name}/{date}/{filename}"


class UserProfile(models.Model):

    GENRE_CHOICES = (
        ('m', 'Мужской'),
        ('f', 'Женский'),
    )
    user = models.OneToOneField(User, verbose_name="Пользователь", related_name="profile", on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name="Телефон")
    first_name = models.CharField(
        max_length=124,
        verbose_name='Имя',)
    Last_name = models.CharField(
        max_length=124,
        verbose_name='Фамилия',)
    photo = models.ImageField(
        blank=True,
        null=True,
        upload_to=upload_to,
        verbose_name='фото'
    )
    birth_date = models.DateField(null=True, verbose_name='дата рождения')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, verbose_name='страна')
    gender = models.CharField(max_length=1, choices=GENRE_CHOICES, null=True, verbose_name='пол')

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         UserProfile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
