from tasks import add

result = add.delay(4, 6)
print(f'Task result: {result.get(timeout=10)}')
