from queue import Queue
from threading import Thread
from time import time
from os import makedirs, listdir
from wget import download as wdl
from colorama import Fore

from .user import Photo, User, Logger


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
        self.workers: list[Worker] = [Worker(self.queue, function, len(args))
                                      for _ in range(workers_num)]

    def run(self):
        ts = time()
        for arg in self.args:
            self.queue.put(arg)
        self.queue.join()
        return round(time() - ts, 2)


class Downloader:
    def __init__(self, download_dir: str = 'downloads', workers=10) -> None:
        self.download_dir = download_dir
        self.workers = workers
        self.logger = Logger('Downloader')

    def download(self, user: User):
        path = f'{self.download_dir}/{user.username}/'
        photos = user.photos
        try:
            makedirs(path)
        except FileExistsError:
            downloaded = listdir(path)
            photos = [photo for photo in photos
                      if photo.filename not in downloaded]

        def function(photo: Photo):
            wdl(photo.url, path + photo.filename, None)

        if photos:
            self.logger.info(f'{Fore.BLUE} downloading '
                             f'{Fore.GREEN}{len(photos)} {Fore.BLUE}photos')
            threader = Threader(self.workers, function, photos)
            tf = threader.run()
            self.logger.info(f'{Fore.BLUE} finished in '
                             f'{Fore.GREEN}{tf} {Fore.BLUE}seconds')
