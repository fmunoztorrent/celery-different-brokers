from celery import Celery

app = Celery('celery_app')
app.config_from_object('celeryconfig')

# Import tasks to register in celery
import tasks
