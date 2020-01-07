'''
Created on 28 giu 2017

@author: stefano
'''

import collections

Transition = collections.namedtuple('Transition','name prev trig cond next acts')

Message = collections.namedtuple('Message','channel kind arguments')

Stat = collections.namedtuple('Stat','mean variance min max count')

def str2msg(msgString):
    (cchan,payload) = tuple(msgString.split('!'))
    (mmsg,arglist) = tuple(payload.split('<'))
    aargs = arglist.split('|')
    temp = aargs[-1]
    temp = temp[0:-1]
    aargs[-1] = temp
    retval = Message(channel=cchan,kind=mmsg,arguments=aargs)
    return retval
    
def payload2str(p):
    retval = p.kind + '<' 
    for a in p.arguments:
        retval = retval + str(a) + '|'
    retval = retval[0:-1] + '>'
    return retval

def changeEventUnroll(s):
    return s[1:-1] + ' != ' + s[1:-1] + '_old'

def subs(d,s):
    retval = s
    ks = d.keys()
    flag = s in ks
    if flag:
        retval = d[s]
    return retval

def xor(a,b):
    return (a and not(b)) or (b and not(a))