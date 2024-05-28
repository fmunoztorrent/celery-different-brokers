from tasks import add

result = add.delay(4, 4)
print('Task enqueued, waiting for result...')
print('Result:', result.get(timeout=10))
