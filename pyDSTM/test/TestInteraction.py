'''
Created on 03 lug 2017

@author: stefano
'''

from ModelFactory import ModelFactory
import sys
from Interactive import Interactive

def tstGetMessage():
    factory = ModelFactory()
    consumer = factory.generation('00_consumer.ini')
    producer = factory.generation('00_producer.ini')
    executor = Interactive()
    executor.addModel(consumer)
    executor.addModel(producer)
    executor.run()
    print consumer.observations
    print 'len ' + str(len(consumer.observations))
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
