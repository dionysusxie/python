#!/usr/bin/env python -u

import math as foobar
from math import sqrt


print 'La la la ...',
print 'I ma Dio Xie.'
print foobar.sqrt(9)

x = 2

if x != 2:
    print 'x != 2'
else:
    pass
    print 'x == 2'


# Exec
scope = {}
exec 'sqrt = 1' in scope
print 'sqrt(4) = ' + str(sqrt(4))
print 'scope.sqrt = ' + str(scope['sqrt'])
print 'scope.keys:', scope.keys()


# doc of a method
def helloWorld():
    'To print out "Hello world!"'
    print 'Hello world!'
helloWorld()
print 'helloWorld.__doc__: ' + helloWorld.__doc__

#
def printParams4(x, y, z=3, *pospar, **keypar):
    print
    print x, y, z
    print pospar
    print keypar

printParams4(1, 2, 3, 5, foo=1, bar=2)
printParams4(1, 2, 3, 5, 6, 7, foo=1, bar=2)
printParams4(1, 2, 3, 5, 6, 7, foo=1, bar=2, name='Dio Xie')
printParams4(1, 2)


# a method returning a tuple
print
def returnATuple():
    return (1, 2, 3)
r1 = returnATuple()
print r1

print
def returnATuple2():
    return (1,)
r1 = returnATuple2()
print r1

#
print
def add(x, y):
    return x + y
print add(*(1, 2))

#
print
def hello(name, greeting):
    return greeting + ', ' + name + '!'
print hello('Dio', 'Hello')
greet = {'name': 'Dio', 'greeting': 'Hi'}
print hello(**greet)


#
# nested function
#

print

def multiplier(factor):
    def multiplyByFactor(number):
        print '%s * %s = %d' % (number, factor, number*factor)
    return multiplyByFactor

double = multiplier(2)
double(1), double(2), double(3)
multiplier(5)(4), multiplier(5)(5), multiplier(5)(6)


#
# filter
#

print
def twentys(num):
    return 20 <= num < 30

nums = [1, 45, 29, 28, 11, 20, 30]
print nums
print 'filter :', filter(twentys, nums)
print 'seq    :', [n for n in nums if 20 <= n < 30]
print 'lambda :', filter(lambda n: 20 <= n < 30, nums)


#
# reduce
#

print
nums = (1, 2, 3, 4, 5)
print 'sum of', nums, 'is:', reduce(lambda x, y: x+y, nums)

