from celery import Celery

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    return x + y

# Enviar la tarea
if __name__ == "__main__":
    result = add.delay(4, 6)
    print(f'Task result: {result.get(timeout=30)}')
