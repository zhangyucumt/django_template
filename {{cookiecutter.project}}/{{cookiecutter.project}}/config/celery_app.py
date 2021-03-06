import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.project}}.config.settings")

app = Celery("{{cookiecutter.project}}")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True, name='test.name')
def test(self, x, y):
    import logging
    logger = logging.getLogger(__name__)

    logger.info("gogoggo")

    print(self.request.id)
    return x + y

@app.task(bind=True)
def test_db_sleep_task(self):
    from django.db import connections
    with connections['default'].cursor() as cursor:
        cursor.execute("select sleep(30)")
        row = cursor.fetchone()
    return {'result': 1}
