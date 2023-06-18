import os
import sys
from celery import Celery

app = Celery('Django_Restaurant')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Restaurant.settings')

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)


@app.task
def schedule_delete_non_compliant_reservations():
    from admin_app.tasks import delete_non_compliant_reservations

    delete_non_compliant_reservations.apply_async(countdown=3600)
