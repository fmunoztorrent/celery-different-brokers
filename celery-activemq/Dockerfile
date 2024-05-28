FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Instalar netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

RUN useradd -ms /bin/bash celeryuser

COPY . /app/
COPY stomp_transport.py /app/stomp_transport.py
COPY wait-for-activemq.sh /app/wait-for-activemq.sh
COPY test_stomp_connection.py /app/test_stomp_connection.py

# Asegurarse de que el script tenga permisos de ejecución
RUN chmod +x /app/wait-for-activemq.sh

RUN chown -R celeryuser:celeryuser /app

USER celeryuser

ENTRYPOINT ["/app/wait-for-activemq.sh", "activemq", "celery", "-A", "tasks", "worker", "--loglevel=info"]
