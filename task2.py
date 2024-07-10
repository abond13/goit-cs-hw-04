from multiprocessing import Process, Queue
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

def search_in_file(file_path, keywords, results_queue):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results_queue.put((keyword, file_path))
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except IOError as e:
        print(f"Error: Could not read file {file_path}. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")    

def process_task(files, keywords, results_queue):
    for file in files:
        search_in_file(file, keywords, results_queue)


def main_multiprocessing(file_paths, keywords):
    num_processes = 4 
    processes = []
    results_queue = Queue()
    results = defaultdict(list)
    file_paths_per_process = round_robin_distribute(file_paths, num_processes)

    start = time.time()
    for i in range(num_processes):
        process = Process(target=process_task, args=(file_paths_per_process[i], keywords, results_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    end = time.time()
    print(f"Search Time: {end - start}\n\n")

    while not results_queue.empty():
        keyword, file_path = results_queue.get()
        results[keyword].append(file_path)

    return results


if __name__ == '__main__':
    file_paths = list(Path("texts").glob("*.txt"))
    keywords = ['of', 'grammar', 'hat', 'ye']

    results = main_multiprocessing(file_paths, keywords)
    print(f"Search Results:\n{results}")
