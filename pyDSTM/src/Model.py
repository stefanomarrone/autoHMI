'''
Created on 21 giu 2017
@author: Stefano Marrone
'''

import re
import copy
import numpy
import Utils
from DSTMreader import DSTMreader
from DSTMwriter import DSTMwriter

class Model(object):
    '''
    This is a base class implementing the base behaviour of a DSTM model
    @nname String name of the DSTM machine
    @pperiod integer Scheduling period of the cycle of the machine in milliseconds
    @inboundChannels [(n,port)] list of tuples representing the inbound channels of the machine where n is the name of the channel
    and port is the local port at which accept to connections
    @outboundChannels [(n,address,port)] list of tuples representing the outbound channels of the machine where n is the name of the channel,
    address is the remote machine to connect and port is the remote port at which connect
    @varlist [n] names of the local variable of the machine
    @delta [(ps, t, c, a, ns)] is the list of the transitions in the model. Each transition is a named tuple...
    @initial initial state of the machine    
    '''
    def __init__(self, nname, dbgflag, pperiod, inboundChannels, outboundChannels, varlist, delta, initial, obs, stats, events):
        self.name = nname
        self.debugFlag = dbgflag
        self.state = ''
        self.behav = list()
        self.data = dict()
        self.reader = None
        self.writer = None
        self.inboundmsg = list()
        self.outboundmsg = list()
        self.cycletime = pperiod
        self.cyclecount = 0
        self.toStat = stats
        self.observable = obs
        self.observations = list()
        self.events = events
        self.eventTime = dict()
        self.md = {'<ASND>': self.manageChanSend, '<AASS>': self.manageVarAssign, '<AGET>': self.getMessage, '<ARCV>': self.recvMessage}
        self.initData(varlist)
        self.initSM(delta,initial)
        self.initIO(inboundChannels,outboundChannels)
        self.initStat()
        
    def debug(self, log):
        if (self.debugFlag == True):
            print '(' + self.name + '@' + str(self.cyclecount) + ')' + log
     
    def dump(self, log):
        if (self.debugFlag == True):
            print log

    # Functions devoted to the initialization of the State Machine
    def initSM(self,d,i):
        self.behav = d
        self.state = i

    # Functions devoted to the initialization of the communication channels
    def initIO(self,icl,ocl):
        self.reader = map(lambda c: DSTMreader(c,self.inboundmsg),icl) 
        self.writer = DSTMwriter(ocl,self.outboundmsg)

    def initStat(self):
        self.statistics = dict()
        for s in self.toStat:
            self.statistics[s] = list()

    def initEvents(self):
        self.eventTime = dict()
        for e in self.events:
            self.eventTime[e] = list()

    # Functions devoted to the initialization of the varible register
    def resetData(self,l):
        self.data[l] = ''

    def initData(self,v):
        map(lambda l: self.resetData(l),v)
            
    def getTrigger(self):
        recvd = copy.deepcopy(self.inboundmsg)
        internals = filter(lambda r: r.isInternal(),self.reader)
        internals = map(lambda r: r.getChannel(),internals)
        for msg in recvd:
            if (msg[0] in internals):
                temp = filter(lambda m: m[0] == msg[0],recvd)
                if (len(temp) > 1):
                    temp = temp[1:]
                    for t in temp:
                        i = recvd.index(t)
                        del recvd[i]
        if (len(recvd) == 0):
            recvd = list()
            recvd.append('')
        return recvd
    
    def singleMatch(self,r,m):
        retval = (r[0] == m[0]) and ((r[1] == '-') or (r[1] == m[1]))
        return retval

    def matchTrigger(self,recv,todo):
        if ((todo == '') or (recv == '')):
            retval = (todo == '')
        else:
            (recvcha, recvmsg,intext) = recv
            recv = (recvcha, recvmsg[0:recvmsg.index('<')],intext)
            refined = todo.replace('<T',"""self.singleMatch(recv,('""")
            refined = refined.replace('/',"""','""")
            refined = refined.replace('T>',"""'))""")
            retval = eval(refined)
        return retval

    def matchTriggers(self,recvs,todo):
        retval = False
        if len(recvs) > 1:
            outcomes = map(lambda r: self.matchTrigger(r,todo),recvs)
            retval = reduce(lambda a,b: a or b, outcomes)
        else:
            retval = self.matchTrigger(recvs[0],todo)
        return retval

    def applyCondition(self,cond):
        refined = cond.replace('<C','self.')
        refined = refined.replace('C>','')
        return eval(cond,globals(),self.data)        

    def manageVarAssign(self,action):
        exec(action,globals(),self.data)    
    
    def microeval(self,s):
        return eval(s,globals(),self.data)
        
    def manageChanSend(self,action):
        msg = Utils.str2msg(action)
        res = map(lambda p: self.microeval(p),msg.arguments)
        newmsg = Utils.Message(msg.channel,msg.kind,res)
        msgtxt = Utils.payload2str(newmsg)
        self.outboundmsg.append((newmsg.channel,msgtxt))
    
    def singleAssign(self,var,val):
        if (var != '_'):
            self.data[var] = val
    
    def popChannel(self,chname):
        i = 0
        flag = False
        while (not flag) and (i < len(self.inboundmsg)):
            temp = self.inboundmsg[i]
            flag = (temp[0] == chname)
            if flag:
                del self.inboundmsg[i]
            i+=1
    
    def computeMessage(self,action,flag):
        temp = self.getTrigger()
        temp = map(lambda t: t[0] + '!' + t[1],temp)
        recv = map(lambda t: Utils.str2msg(t),temp)
        temp = action.replace('?','!')
        verf = Utils.str2msg(temp)
        recv = filter(lambda r: (r.channel == verf.channel) and (r.kind == verf.kind),recv)
        recv = recv[0]
        map(lambda var, val: self.singleAssign(var,val),verf.arguments,recv.arguments)
        if flag:
            intchannels = map(lambda r: r.getChannel(),filter(lambda r: r.isInternal(),self.reader))
            if (verf.channel in intchannels):
                self.popChannel(verf.channel) 
    
    def getMessage(self,action):
        self.computeMessage(action,True)
    
    def recvMessage(self,action):
        self.computeMessage(action,False)

    def record(self,transname):
        current = dict()
        current['currentstate'] = self.state
        current['transition'] = transname
        for o in self.observable:
            current[o] = eval(o,globals(),self.data)
        self.observations.append(current)

    def recordStat(self):
        for s in self.toStat:
            self.statistics[s].append(eval(s,globals(),self.data))

    def getStat(self):
        retval = dict()
        for s in self.toStat:
            temp = self.statistics[s]
            temp = filter(lambda t: t != '',temp)
            temp = map(lambda t: float(t),temp)
            meanVal = numpy.mean(temp)
            varVal = numpy.var(temp)
            minVal = numpy.min(temp)
            maxVal = numpy.max(temp)
            countVal = len(temp)
            item  = Utils.Stat(mean = meanVal, variance = varVal, min = minVal, max = maxVal, count = countVal)
            retval[s] = item
        return retval

    def checkEvents(self,backup):
        createflag = False
        varStatus = self.data.copy()
        for k in backup.keys():
            varStatus[k + '_old'] = backup[k]
        for s in self.events:
            temp = s
            pattern = re.compile('\{\w*\}')
            matches = pattern.findall(s)
            injections = map(lambda x: Utils.changeEventUnroll(x),matches)
            for i in range(0,len(matches)):
                s = s.replace(matches[i],injections[i])
            pattern = re.compile('\w*')
            matches = pattern.findall(s)
            matches = filter(lambda pp: pp != '',matches)
            injections = map(lambda x: Utils.subs(varStatus,x),matches)
            if (not('' in injections)):
                fflag = False                
                for j in range(0,2):  
                    for i in range(0,len(matches)):
                        if (Utils.xor(fflag,matches[i].endswith('_old'))):
                            s = s.replace(matches[i],injections[i])
                    fflag = not(fflag)
                flag = eval(s)
                if (flag == True):
                    if (createflag == False):
                        createflag = True
                        self.eventTime[self.cyclecount] = list()
                    self.eventTime[self.cyclecount].append(temp)

    def getEvents(self):
        return self.eventTime

    def manageAction(self,action):
        if (action != ''):
            ks = self.md.keys()
            nums = range(0,len(ks))
            index = filter(lambda i: action.startswith(ks[i]),nums)[0]
            action = action.replace(ks[index],'')
            f = self.md[ks[index]]
            f(action) 
    
    def applyActions(self,actions):
        map(lambda a: self.manageAction(a),actions.split(';'))
        
    def cleanChannels(self):
        del self.inboundmsg[:]
