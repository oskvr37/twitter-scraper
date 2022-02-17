from queue import Queue
from threading import Thread
from time import time


class Worker(Thread):
    def __init__(self, queue, function, args_len):
        Thread.__init__(self)
        self.queue: Queue = queue
        self.function = function
        self.args_len = args_len
        self.daemon = True
        self.start()
        
    def run(self):
        while True:
            arg = self.queue.get()
            try:
                self.function(arg)
            except Exception as e:
                print(f'Worker failed\t({e})')
            finally:
                self.queue.task_done()


class Threader:
    def __init__(self, workers_num: int, function, args: list) -> None:
        self.args = args
        self.queue = Queue()
        self.workers: list[Worker] = [Worker(self.queue, function, len(args)) for _ in range(workers_num)]
        
    def run(self):
        ts = time()
        for arg in self.args: self.queue.put(arg)
        self.queue.join()
        return round(time() - ts, 2)
