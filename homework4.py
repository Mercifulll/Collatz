import multiprocessing
import itertools

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

def calculate_collatz_range(numbers, results, start, end):
    local_results = []
    for num in itertools.islice(numbers, start, end):
        steps = collatz_steps(num)
        local_results.append(steps)
    results.extend(local_results)

if __name__ == "__main__":
    N = int(input("Введіть натуральне число: "))
    num_processes = 10

    numbers = list(range(1, N + 1))
    results = multiprocessing.Manager().list()

    # Розділити числа на частини для обробки
    chunk_size = len(numbers) // num_processes
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]

    processes = [multiprocessing.Process(target=calculate_collatz_range, args=(numbers, results, start, end)) for start, end in chunks]

    # Запустити процеси
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    # Порахувати середню кількість кроків
    average_steps = sum(results) / len(numbers)
    print(f"Середня кількість кроків для {N} = {average_steps}")
