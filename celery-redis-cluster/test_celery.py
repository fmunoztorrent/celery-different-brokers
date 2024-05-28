from tasks import add

if __name__ == "__main__":
    result = add.delay(4, 6)
    print("Task result:", result.get())
