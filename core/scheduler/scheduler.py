import os
from threading import Thread
from queue import Queue
from core.fs import log
import time

from core.scheduler.task import Task


class Scheduler():
    """
    Schedules tasks to be run in parallel.
    **It should never call outside functions** but be called from outside!
    """

    queue = Queue()
    poll_time = 5
    _worker_thread: Thread = None
    _periodic_tasks: list[object] = []

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        log.info("Starting Job scheduler...")
        self._worker_thread = Thread(target=self._worker, daemon=True)
        self._worker_thread.start()


    def register_task(self, task: Task):
        self.queue.put(task)


    def register_independent_task(self, method):
        """
        Runs a method in parallel, without depending on a queue. Perfect for periodic tasks.
        :param method: Function to be run
        """
        th = Thread(target=method, daemon=True)
        self._periodic_tasks.append(th)
        th.start()


    def _worker(self):
        log.debug("Starting worker...")
        while True:
            job = self.queue.get()
            job.start()
            self.queue.task_done()
            time.sleep(self.poll_time)


scheduler: Scheduler = None

def get_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = Scheduler()
    return scheduler
