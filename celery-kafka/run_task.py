# run_task.py

from celery_app import add

# Ejecutar una tarea
result = add.delay(4, 6)
print('Task result:', result.get(timeout=10))