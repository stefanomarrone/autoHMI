'''
Created on 21 giu 2017
@author: Stefano Marrone
'''

from Batch import Batch

class LimitedBatch(Batch):
    def __init__(self,maxi):
        Batch.__init__(self)
        self.stopCycle = maxi
    
    def until(self,params):
        return (params < self.stopCycle)