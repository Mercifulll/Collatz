import threading

mutex = threading.Lock()
import queue

myQueue = queue.Queue()

# Функція для обчислення кількості кроків до виродження в 1 за гіпотезою Коллатца
def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def calculate_collatz_range(numbers, results):
    while True:
        if myQueue.empty():
            break
        num = myQueue.get()
        steps = collatz_steps(num)
        mutex.acquire()
        try:
            results.append(steps)
        finally:
            mutex.release()


if __name__ == "main":
    N = int(input("Введіть натуральне число: "))
    num_threads = 10

    numbers = list(range(1, N + 1))

    for item in numbers:
        myQueue.put(item)
    
    results = []

    threads = [threading.Thread(target=calculate_collatz_range, args=(numbers, results)) for _ in range(num_threads)]

    # Запустити потоки
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Порахувати середню кількість кроків
    average_steps = sum(results) / len(numbers)
    print(f"Середня кількість кроків для {N} = {average_steps}")