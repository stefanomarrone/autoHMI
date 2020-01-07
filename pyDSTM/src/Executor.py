'''
Created on 21 giu 2017
@author: Stefano Marrone
'''

import time
import random
from Queue import Queue 

class Executor(object):
    def __init__(self):
        self.models = list()
        self.queue = Queue()
    
    def addModel(self,model):
        self.models.append(model)

    def doWork(self):
        mdl = self.queue.get()
        self.singlerun(mdl)
        self.queue.task_done()

    def singlerun(self,mdl):
        map(lambda x: x.start(),mdl.reader)
        mdl.writer.start()
        mdl.observations = list()
        while(self.until(mdl.cyclecount)):
            time.sleep(mdl.cycletime)
            backup = mdl.data.copy()
            mdl.debug('Start cycle in state: ' + mdl.state)
            trigger = mdl.getTrigger()
            rules = filter(lambda l: (l.prev == mdl.state) and mdl.matchTriggers(trigger,l.trig),mdl.behav)
            rules = filter(lambda l: mdl.applyCondition(l.cond),rules)
            trname = ''
            if (len(rules) > 0):
                rule = random.choice(rules)
                trname = rule.name
                mdl.state = rule.next
                mdl.applyActions(rule.acts)
                mdl.debug('Trigger received: ' + rule.trig)
                mdl.debug('Condition ok: ' + rule.cond)
                mdl.debug('Next state: ' + rule.next)
                mdl.debug('Action applied: ' + rule.acts)
            mdl.record(trname)
            mdl.recordStat()
            mdl.checkEvents(backup)
            mdl.cyclecount += 1
            mdl.cleanChannels()        
