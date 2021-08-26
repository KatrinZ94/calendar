import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily.settings')
app = Celery('daily')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'update_public_holidays': {
        'task': 'event.tasks.refresh_public_holiday',
        'schedule': crontab(minute='30', hour='12', day_of_month='1')
    }
}

