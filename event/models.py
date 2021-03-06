from django.contrib.auth.models import User
from django.db import models
import uuid


class Country(models.Model):
    name = models.CharField(
        max_length=124,
        verbose_name='страна'
    )

    def __str__(self):
        return self.name


class UserEvent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='event'
    )
    name = models.CharField(
        max_length=124,
        verbose_name='событие',
        help_text='введите название события'
    )
    start_date = models.DateTimeField(
        db_index=True,
        verbose_name='начало события',
        help_text='введите дату и время начала события'
    )
    end_date = models.DateTimeField(
        null=False,
        blank=True,
        verbose_name='окончание события',
        help_text='введите дату и время окончания события'
    )
    choices_of_time_reminder = (
        (1, 'час'),
        (2, '2 часа'),
        (4, '4 часа'),
        (24, 'день'),
        (168, 'неделю')
    )
    reminder_before = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name='напоминание о событии',
        help_text='выберите время напоминания',
        choices=choices_of_time_reminder
    )


class PublicHoliday(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=300,
        verbose_name='название государственного праздника',
    )
    start_date = models.DateTimeField(
        db_index=True,
        verbose_name='начало праздника',
    )
    end_date = models.DateTimeField(
        null=False,
        blank=True,
        verbose_name='окончание праздника',
    )


class Task (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, )
    event = models.ForeignKey(UserEvent, on_delete=models.CASCADE)
