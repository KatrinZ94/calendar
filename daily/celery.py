import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily.settings')
app = Celery('daily')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
