# Celery with Kafka Setup

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```
.
├── docker-compose.yml
├── Dockerfile
├── celery_app.py
├── tasks.py
├── run_task.py
└── requirements.txt
```

## Dockerfile

```dockerfile
FROM python:3.9-slim

# Crear un usuario no root
RUN groupadd -r celery && useradd -r -g celery celery

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos y la configuración de Celery al contenedor
COPY requirements.txt requirements.txt
COPY celeryconfig.py celeryconfig.py

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Cambiar el usuario a celery
USER celery

# Establecer el comando por defecto para ejecutar Celery
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]

```

## docker-compose.yml

```yaml
version: '3.8'

services:
  zookeeper:
    image: 'bitnami/zookeeper:latest'
    container_name: zookeeper
    ports:
      - '2181:2181'
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes
    mem_limit: 512m

  kafka:
    image: 'bitnami/kafka:latest'
    container_name: kafka
    ports:
      - '9092:9092'
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_LISTENERS=PLAINTEXT://:9092
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
      - ALLOW_PLAINTEXT_LISTENER=yes
    depends_on:
      - zookeeper
    mem_limit: 1g
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  celery:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: celery
    depends_on:
      - kafka
    environment:
      - CELERY_BROKER_URL=confluentkafka://kafka:9092
      - CELERY_RESULT_BACKEND=rpc://
    mem_limit: 512m

```

## requirements.txt

```text
celery==5.2.7
confluent-kafka==1.9.0
```

## celery_app.py

```python
from celery import Celery

app = Celery('celery_app')
app.config_from_object('celeryconfig')

# Import tasks to register in celery
import tasks

```

## tasks.py

```python
from celery_app import app

@app.task
def add(x, y):
    return x + y

```

## run_task.py

```python
from tasks import add

result = add.delay(4, 6)
print(f'Task result: {result.get(timeout=10)}')

```

## Running the Project

### Build and Run the Containers

```bash
docker-compose up --build
```

### Run a Task

In a new terminal, run the following script to execute a task:

```bash
docker-compose run celery python run_task.py
```
