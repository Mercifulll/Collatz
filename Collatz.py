import threading

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
    local_results = []  # Локальний список для зберігання результатів поточного потоку
    for num in numbers:
        steps = collatz_steps(num)
        local_results.append(steps)
    # Додати результати поточного потоку до загального списку
    results.extend(local_results)

if __name__ == "__main__":
    N = int(input("Введіть натуральне число: "))
    num_threads = 10

    numbers = list(range(1, N + 1))
    results = []

    # Розділити числа між потоками
    chunk_size = len(numbers) // num_threads
    threads = []

    # Створити та запустити потоки для обчислень
    for i in range(num_threads):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i != num_threads - 1 else len(numbers)
        thread = threading.Thread(target=calculate_collatz_range, args=(numbers[start_idx:end_idx], results))
        thread.start()
        threads.append(thread)

    # Завершити всі потоки
    for thread in threads:
        thread.join()

    # Порахувати середню кількість кроків
    average_steps = sum(results) / len(numbers)
    print(f"Середня кількість кроків для {N} = {average_steps}")