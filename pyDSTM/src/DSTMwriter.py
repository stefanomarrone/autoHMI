'''
Created on 03 lug 2017
@author: stefano
'''
import threading
import socket
import time

class DSTMwriter(threading.Thread):
    '''
    This is a writer for the DSTM class
    '''
    def __init__(self,cl,msgbuff):
        threading.Thread.__init__(self)
        self.register = dict()
        self.buffer = msgbuff
        self.sleepperiod = 0.01
        map(lambda c: self.socket(c),cl)      

    def socket(self,c):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.register[c[0]] = (s,c[1:])
    
    def pad(self,msg,n):
        retval = msg + n*'*' + '\0'
        return retval
        
    def run(self):
        while True:
            time.sleep(self.sleepperiod)
            if (len(self.buffer)>0):
                send = self.buffer[0]
                self.buffer.remove(send)
                (c,m) = send
                (s,dest) = self.register[c]
                m = self.pad(m,0)
                s.sendto(m,dest)
