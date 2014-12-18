#!/usr/bin/env python -u

__metaclass__ = type

class Person:

    print 'Class Person being defined...'

    num_members = 0

    def __init__(self):
        Person.num_members += 1
        print 'Object number of class Person:', Person.num_members

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def greet(self):
        print 'Hello, world! I am %s.' % self.name

    def accessible(self):
        return self.__inaccessible()

    def __inaccessible(self):
        'Will be converted to _Person__inaccessible()'
        print "Bet you can't see me..."

    def _inaccessible(self):
        'This method will not be imported by "import *" statement!'
        print "Person._inaccessible()"


x = Person()
y = Person()
print x.num_members
print y.num_members

x.setName('Dio Xie')
x.greet()
Person.greet(x)
x.accessible()
x._inaccessible()

print x.name
print "Person's fields:"
print dir(Person)
