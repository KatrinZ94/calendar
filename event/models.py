from django.contrib.auth.models import User
from django.db import models


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


class GarmentEvent:
    def __init__(self, name, _begin, _end_time):
        self.name = name
        self.start_date = _begin
        self.end_date = _end_time


