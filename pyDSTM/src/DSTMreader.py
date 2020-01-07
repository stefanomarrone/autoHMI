'''
Created on 03 lug 2017
This class contains the DSTM reader based on UDP communications
@author: stefano
'''
import threading
import socket

class DSTMreader(threading.Thread):

    def __init__(self, c, buff):
        threading.Thread.__init__(self)
        self.queue = buff
        self.channel = c[0]
        self.source = c[2]
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(('',c[1]))
    
    def getChannelName(self):
        return self.channel
    
    def isInternal(self):
        return (self.source == 'int')        
    
    def recv_all(self):
        data=''
        runflag = True
        while (runflag):
            (more, add) = self.socket.recvfrom(1024)
            data += more
            runflag = not data.endswith('\0')
        return data[0:-1]
    
    def run(self):
        while True:
            data = self.recv_all()
            self.queue.append((self.channel,str(data),self.source))