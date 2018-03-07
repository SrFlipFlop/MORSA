#https://pymotw.com/2/multiprocessing/basics.html
#https://docs.python.org/2/library/multiprocessing.html
#https://noswap.com/blog/python-multiprocessing-keyboardinterrupt
#http://cuyu.github.io/python/2016/08/15/Terminate-multiprocess-in-Python-correctly-and-gracefully

from time import sleep
from datetime import datetime 
from multiprocessing import Process

class EchoModule:
    def __init__(self):
        self.jobs = {}
    
    def create(self, job):
        process = Process(target=self.worker, args=(job,))
        key = len(self.jobs.keys())
        self.jobs[key] = {
            'info': job,
            'process': process,
            'start': datetime.now().strftime('%d-%M-%Y %H:%m:%S'),
            'status': 'Planned',
        }

    def start(self, job):
        self.jobs[job]['process'].start()
        self.jobs[job]['status'] = 'Running'

    def kill(self, job):
        self.jobs[job]['process'].terminate()
        self.jobs[job]['status'] = 'Finished'

    def kill_all(self):
        for job in self.jobs:
            self.kill(job)

    def get_jobs(self):
        return self.jobs

    def worker(self, arg):
        while True:
            print("Echo: {0}".format(arg))
            sleep(1)