from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'time_tracker.settings')

# create a Celery instance and configure it.
app = Celery('time_tracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Add periodic task to update user statistics daily at midnight
app.conf.beat_schedule = {
    'update-user-statistics': {
        'task': 'book.tasks.update_user_reading_statistics',
        'schedule': crontab(hour='0', minute='0'),  # Run daily at midnight
    },
}
