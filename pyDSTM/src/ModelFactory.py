'''
Created on 03 lug 2017

@author: stefano
'''
import ConfigParser
import Utils
from Model import Model

class ModelFactory(object):
    '''
    classdocs
    '''
    def __init__(self):
        self.reader = ConfigParser.ConfigParser()
    
    def getSection(self,s):
        temp = dict()
        options = self.reader.options(s)
        for o in options:
            try:
                temp[o] = self.reader.get(s,o)
                if temp[o] == -1:
                    print("skip: %s" % o)
            except:
                print("exception on %s!" % o)
                temp[o] = None
        return temp
    
    def getObservation(self,d,i):
        return self.getSymbol(d,i,'o_')
    
    def getEvent(self,d,i):
        return self.getSymbol(d,i,'e_')

    def getVariable(self,d,i):
        return self.getSymbol(d,i,'v_')
    
    def getStatistic(self,d,i):
        return self.getSymbol(d,i,'s_')

    def getSymbol(self,d,i,header):
        temp = header + str(i)
        return d[temp]        

    def getIChannel(self,d,i):
        temp = 'ich_' + str(i)
        temp = d[temp]
        temp = temp[1:-1]
        temp = temp.split(',')
        temp = (temp[0],int(temp[1]),temp[2])
        return temp

    def getOChannel(self,d,i):
        temp = 'och_' + str(i)
        temp = d[temp]
        temp = temp[1:-1]
        temp = temp.split(',')
        temp = (temp[0],temp[1],int(temp[2]))
        return temp

    def getTransition(self,d,i):
        temp = 't_' + str(i)
        temp = d[temp]
        temp = temp[1:-1]
        temp = temp.split(',')
        temp = Utils.Transition(name=temp[0],prev=temp[1],trig=temp[2],cond=temp[3],next=temp[4],acts=temp[5])
        return temp

    def getList(self,sectName,f,size):
        td = self.getSection(sectName)
        retval = map(lambda i: f(td,i),range(0,size))
        return retval

    def generation(self,inifilename):
        self.reader.read(inifilename)
        td = self.getSection('Main')                
        nname = td['name']
        ddbg = (td['debug'] == 'True')
        ccycle = float(td['cycle'])
        ts = int(td['transitions'])
        os = int(td['observations'])
        ss = int(td['stats'])
        es = int(td['events'])
        vs = int(td['variables'])
        ics = int(td['inbound'])
        ocs = int(td['outbound'])
        # initial state
        td = self.getSection('States')
        initState = td['initial']
        # lists
        varlist = self.getList('Variables',self.getVariable,vs)
        inbounds = self.getList('Inbound',self.getIChannel,ics)
        outbounds = self.getList('Outbound',self.getOChannel,ocs)
        delta = self.getList('Transitions',self.getTransition,ts)
        observations = self.getList('Observations',self.getObservation,os)
        statistics = self.getList('Statistics',self.getStatistic,ss)
        events = self.getList('Events',self.getEvent,es)
        # create the Model and .....
        model = Model(nname,ddbg,ccycle,inbounds,outbounds,varlist,delta,initState,observations,statistics,events)
        return model 
