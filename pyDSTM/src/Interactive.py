'''
Created on 21 giu 2017
@author: Stefano Marrone
'''

import thread
import numpy
from Executor import Executor

class Interactive(Executor):
    def __init__(self):
        Executor.__init__(self)
    
    def until(self,params):
        self.queue.task_done()
        payload = self.queue.get(True,18*60)
        flag = (payload != None) 
        return flag
    
    def run(self):
        inputs = self.models
        map(lambda x: thread.start_new_thread(self.doWork,()),inputs)
        flag = (int(raw_input("-1 to stop")) != -1)
        while (flag):
            flag = (int(raw_input("-1 to stop")) != -1)
            if (flag == False):
                inputs = numpy.repeat(None,len(inputs))
            map(lambda m: self.queue.put(m),inputs)
            self.queue.join()
