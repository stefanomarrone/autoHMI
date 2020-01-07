'''
Created on 07 lug 2017

@author: stefano
'''

from DSTMreader import DSTMreader
import time

class Sink(object):
    def __init__(self,c):
        self.inboundmsg = list()
        self.ch = c

    def getTrigger(self):
        recvd = ''
        if (len(self.inboundmsg)>0):
            recvd = self.inboundmsg[0]
            self.inboundmsg.remove(recvd)
        return recvd
    
    def run(self):
        self.reader = DSTMreader(self.ch,self.inboundmsg)
        self.reader.start()
        for i in range(0,200):
            print '<SINK'
            print self.getTrigger()
            print 'SINK>'
            time.sleep(0.5)
