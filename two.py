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