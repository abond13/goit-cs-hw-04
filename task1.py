from threading import Thread
import time
from collections import defaultdict
from pathlib import Path

def round_robin_distribute(A, n):
    # Initialize n empty arrays in B
    B = [[] for _ in range(n)]
    
    # Distribute elements from A to B in round-robin fashion
    for i, element in enumerate(A):
        B[i % n].append(element)
    
    return B

def search_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except IOError as e:
        print(f"Error: Could not read file {file_path}. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def thread_task(files, keywords, results):
    for file in files:
        search_in_file(file, keywords, results)


def main_threading(file_paths, keywords):
    num_threads = 4 
    threads = []
    results = defaultdict(list)
    file_paths_per_thread = round_robin_distribute(file_paths, num_threads)

    start = time.time()
    for i in range(num_threads):
        thread = Thread(target=thread_task, args=(file_paths_per_thread[i], keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    end = time.time()
    print(f"Search Time: {end - start}\n\n")

    return results


if __name__ == '__main__':
    file_paths = list(Path("texts").glob("*.txt"))
    keywords = ['of', 'grammar', 'hat', 'ye']

    results = main_threading(file_paths, keywords)
    print(f"Search Results:\n{results}")
