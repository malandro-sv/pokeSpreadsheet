#!/usr/bin/env python

import threading
import queue

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

threading.Thread(target=worker, daemon=True).start()

for item in range(30):
    q.put(item)

q.join()
print('All work completed')

