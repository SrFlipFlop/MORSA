#https://pymotw.com/2/multiprocessing/basics.html
#https://docs.python.org/2/library/multiprocessing.html
#https://noswap.com/blog/python-multiprocessing-keyboardinterrupt
#http://cuyu.github.io/python/2016/08/15/Terminate-multiprocess-in-Python-correctly-and-gracefully

from time import sleep
from datetime import datetime 
from multiprocessing import Process

class Echo:
    def __init__(self):
        self.jobs = {}
        self.words =  ['help', 'run', 'kill', 'killAll', 'showInfo']

    def run(self, user_input):
        if user_input == 'help':
            self.print_help()
        
        elif user_input == 'run':
            arg = user_input.split(' ')[1]
            self.start(arg)

        elif user_input == 'kill':
            arg = user_input.split(' ')[1]
            self.kill(arg)

        elif user_input == 'killAll':
            for job in self.jobs:
                self.kill(job)

        else:
            print('[-] Option "{0}" not found. Please use "help" to see the correct options.'.format(user_input))

    def print_help(self):
        #TODO: print help
        pass

    def start(self, arg):
        process = Process(target=self.worker, args=(arg,))
        key = len(self.jobs.keys())
        self.jobs[key] = {
            'info': job,
            'process': process,
            'start': datetime.now().strftime('%d-%M-%Y %H:%m:%S'),
            'status': 'Running',
        }
        process.start()
        print('[+] Created new job with ID {0}'.format(key))

    def kill(self, job):
        self.jobs[job]['process'].terminate()
        self.jobs[job]['status'] = 'Finished'  

    def show_info(self):
        print('[+] Running jobs:')
        for key, job in self.jobs.iteritems():
            print('\tID: {0} | Start time: {1} | Status: {2}'.format(key, job['start'], job['status']))

    def worker(self, arg):
        while True:
            print("Echo: {0}".format(arg))
            sleep(1)