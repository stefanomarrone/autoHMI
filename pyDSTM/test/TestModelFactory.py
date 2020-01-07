'''
Created on 03 lug 2017

@author: stefano
'''

from ModelFactory import ModelFactory
import os
import sys

def tstABC():
#    configs = ['Alice.ini', 'Bob.ini', 'Charlies.ini']
#     configs = ['Alice.ini','Bob.ini']
#     pids = list()
#     for i in range(0,len(configs)):
#         pids.append(Process(target=spawn, args=(configs[i],)))
#     map(lambda p: p.start(),pids)
#     map(lambda p: p.join(),pids)
    return True

def tstGetMessage():
    pid = os.fork()
    factory = ModelFactory()
    if (pid == 0):
        ps = factory.generation('00_consumer.ini')
        outcomes = ps.limitedRun(30)
        print 'Consumer'
        print ps.getStat()
        print ps.getEvents()
        print outcomes
        sys.exit(0)
    else:
        ps = factory.generation('00_producer.ini')
        outcomes = ps.limitedRun(30)
        os.waitpid(pid,0)
        print 'Producer'
        print outcomes
    return True

def runtest(s):
    fname = s + '()'
    outcome = eval(fname)
    message = str(outcome) + '\t' + s
    print message
    return outcome 

def main():
    tests = ['tstGetMessage']
    map(lambda t: runtest(t),tests)

if __name__ == "__main__":
    main()
    sys.exit(0)
