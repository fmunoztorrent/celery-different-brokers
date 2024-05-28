# celeryconfig.py

broker_url = 'confluentkafka://localhost:9092'  # URL de tu servidor Kafka
result_backend = 'rpc://'  # Puedes usar cualquier backend de resultados compatible
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True