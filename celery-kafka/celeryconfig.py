from celery import Celery
from kombu import Exchange, Queue

app = Celery('celery_app')

# Configure Celery to use Kafka as broker
app.conf.update(
    broker_url='confluentkafka://kafka:9092',
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_default_queue='default',
    task_queues=(
        Queue('default', Exchange('default'), routing_key='default'),
    ),
    broker_transport_options={
        'producer': {
            'bootstrap.servers': 'kafka:9092'
        },
        'consumer': {
            'bootstrap.servers': 'kafka:9092',
            'group.id': 'celery',
            'auto.offset.reset': 'earliest'
        }
    }
)
