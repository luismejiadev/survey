import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')

app = Celery('app_survey')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update({
    'imports': (
        'surveys.tasks',
    ),
    'task_routes': ('surveys.task_router.SurveyRouter',),
})
app.autodiscover_tasks()
