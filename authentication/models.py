from django.contrib.auth.models import User
from django.db import models
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
    birth_date = models.DateField(null=True, verbose_name='дата рождения')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, verbose_name='страна')
    gender = models.CharField(max_length=1, choices=GENRE_CHOICES, null=True, verbose_name='пол')

