FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN useradd -m celeryuser
RUN chown -R celeryuser:celeryuser /app
USER celeryuser

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
