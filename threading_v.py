import threading
import time
from collections import defaultdict

# Функція для вимірювання часу обробки файлу та пошуку ключових слів
def search_keywords_in_file(file_path, keywords, results, times):
    start_time = time.time()  # Початок таймера
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().lower()  # Приведення тексту до нижнього регістру
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Помилка при обробці файлу {file_path}: {e}")
    end_time = time.time()  # Кінець таймера
    times[file_path] = end_time - start_time  # Збереження часу виконання для файлу

# Функція для запуску потоків
def threaded_search(file_list, keywords):
    results = defaultdict(list)
    times = {}  # Час виконання для кожного файлу
    threads = []

    for file in file_list:
        thread = threading.Thread(target=search_keywords_in_file, args=(file, keywords, results, times))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results, times

if __name__ == "__main__":
    start_time = time.time()

    files = ["file1.txt", "file2.txt", "file3.txt"]
    keywords = ["культура", "музика", "традиції", "літак", "подорож"]


    result, times = threaded_search(files, keywords)

    end_time = time.time()
    
    print(f"Результати пошуку: {dict(result)}")
    for file, exec_time in times.items():
        print(f"Час обробки {file}: {exec_time:.6f} сек")
    print(f"Загальний час виконання: {end_time - start_time:.6f} сек")
