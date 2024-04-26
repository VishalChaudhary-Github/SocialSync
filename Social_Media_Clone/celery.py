from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Social_Media_Clone.settings')

app = Celery('Social_Media_Clone')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()