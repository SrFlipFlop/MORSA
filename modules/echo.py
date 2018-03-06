#https://pymotw.com/2/multiprocessing/basics.html
#https://docs.python.org/2/library/multiprocessing.html

from time import sleep
from os import getppid, getpid
from multiprocessing import Process

PROCESS = None

def worker(arg):
    while True:
        print("Echo: {0}".format(arg))
        sleep(1)

def start(process):
    process.start()

def kill(process):
    process.terminate()

def create(arg1):
    global PROCESS
    PROCESS = Process(target=worker, args=(arg1,))

MODULE_OPTIONS = {
    'create': create,
    'start': start,
    'kill': kill    
}

#MODULE_OPTIONS['create'](1)
#print('Created')
#MODULE_OPTIONS['start'](PROCESS)
#print('Time to sleep')
#sleep(5)
#print('Kill')
#MODULE_OPTIONS['kill'](PROCESS)
#print('End')

class EchoModule:
    def __init__(self, arg1=1):
        self.process = Process(target=self.worker, args=(arg1,))
    
    def start(self):
        self.process.start()

    def kill(self):
        self.process.terminate()

    def worker(self):
        while True:
            print("Echo: {0}".format(arg))
            sleep(1)

m = EchoModule(1)
m.start()
sleep(5)
m.kill()