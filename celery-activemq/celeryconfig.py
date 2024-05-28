import os
from kombu import Exchange, Queue, transport
from stomp_transport import Transport

transport.TRANSPORT_ALIASES['stomp'] = 'stomp_transport.Transport'

broker_url = f"stomp://{os.getenv('ACTIVEMQ_USERNAME')}:{os.getenv('ACTIVEMQ_PASSWORD')}@{os.getenv('ACTIVEMQ_HOST')}:{os.getenv('ACTIVEMQ_PORT')}/"
result_backend = 'db+sqlite:///results.sqlite'

task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
)

task_transport_options = {
    'transport': 'stomp',
}

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True
