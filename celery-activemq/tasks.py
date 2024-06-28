from celery import Celery
import logging

app = Celery('tasks')
app.config_from_object('celeryconfig')

app.conf.update(
    task_default_retry_delay=30,  # 30 segundos de delay entre reintentos
    task_max_retries=3,  # Número máximo de reintentos
)

@app.task
def add(x, y):
    logging.info(f'Executing task add with arguments: {x}, {y}')
    return x + y
