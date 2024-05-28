from celery import Celery

app = Celery('tasks', broker='redis://172.28.0.9:22122/0', backend='redis://172.28.0.9:22122/0')

app.conf.update(
    redis_max_connections=100,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@app.task
def add(x, y):
    return x + y
