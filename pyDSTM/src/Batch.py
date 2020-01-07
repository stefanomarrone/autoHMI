'''
Created on 21 giu 2017
@author: Stefano Marrone
'''

import thread
from Executor import Executor

class Batch(Executor):
    def __init__(self):
        Executor.__init__(self)
        
    def run(self):
        for m in self.models:
            thread.start_new_thread(self.doWork,())
            self.queue.put(m)
        self.queue.join() 