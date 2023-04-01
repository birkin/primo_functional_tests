"""
From <https://stackoverflow.com/a/61265000>.
"""

import multiprocessing
import time
from multiprocessing import Process, Lock


def task(n: int, lock):
    with lock:
        print(f'n={n}')
    time.sleep(0.25)


if __name__ == '__main__':
    multiprocessing.set_start_method('forkserver')
    lock = Lock()
    processes = [Process(target=task, args=(i, lock)) for i in range(20)]
    print( 'starting processes...' )
    for process in processes:
        process.start()
    print( 'joining processes...' )
    for process in processes:
        process.join()
