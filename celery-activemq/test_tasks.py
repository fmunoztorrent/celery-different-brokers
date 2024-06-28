from tasks import add

result = add.delay(1, 1)
print('Task enqueued, waiting for result...')
try:
    result_value = result.get(timeout=10)
    print('Result:', result_value)
except Exception as e:
    print(f'Error retrieving result: {e}')
