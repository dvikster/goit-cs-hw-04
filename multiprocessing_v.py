import multiprocessing
import time
from collections import defaultdict

# Функція для пошуку ключових слів у файлі та вимірювання часу обробки
def search_keywords_in_file(file_path, keywords, queue, times_queue):
    start_time = time.time()  # Початок таймера
    result = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().lower()  # Приведення тексту до нижнього регістру
            for keyword in keywords:
                if keyword in content:
                    result.setdefault(keyword, []).append(file_path)
    except Exception as e:
        print(f"Помилка при обробці файлу {file_path}: {e}")
    
    end_time = time.time()  # Кінець таймера
    times_queue.put((file_path, end_time - start_time))  # Збереження часу виконання для файлу
    if result:
        queue.put(result)

# Функція для запуску процесів
def multiprocessing_search(file_list, keywords):
    queue = multiprocessing.Queue()
    times_queue = multiprocessing.Queue()
    processes = []

    for file in file_list:
        process = multiprocessing.Process(target=search_keywords_in_file, args=(file, keywords, queue, times_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = defaultdict(list)
    times = {}

    while not queue.empty():
        partial_result = queue.get()
        for key, value in partial_result.items():
            results[key].extend(value)

    while not times_queue.empty():
        file, exec_time = times_queue.get()
        times[file] = exec_time

    return results, times

if __name__ == "__main__":
    start_time = time.time()

    files = ["file1.txt", "file2.txt", "file3.txt"]
    keywords = ["культура", "музика", "традиції", "літак", "подорож"]


    result, times = multiprocessing_search(files, keywords)

    end_time = time.time()
    
    print(f"Результати пошуку: {dict(result)}")
    for file, exec_time in times.items():
        print(f"Час обробки {file}: {exec_time:.6f} сек")
    print(f"Загальний час виконання: {end_time - start_time:.6f} сек")
