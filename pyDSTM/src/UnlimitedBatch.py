'''
Created on 21 giu 2017
@author: Stefano Marrone
'''

from Batch import Batch

class UnlimitedBatch(Batch):
    def __init__(self):
        Batch.__init__(self)
    
    def until(self,params):
        return True