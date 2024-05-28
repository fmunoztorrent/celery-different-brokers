# celery_app.py

from celery import Celery

app = Celery('my_app')
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    return x + y
