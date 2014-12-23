#!/usr/bin/env python -u

import exceptions

print dir(exceptions)
print

# raise ArithmeticError


class SomeCustomException(Exception):
    def __init__(self):
        Exception.__init__(self, 'It is me.')

# raise SomeCustomException


try:
    x = input('Enter the first number: ')
    y = input('Enter the second number: ')
    print x / y
# except ZeroDivisionError:
#     print 'The second number can\'t be zero!'
# except TypeError:
#     print "That wasn't a number, was it?"
# except (ZeroDivisionError, TypeError, NameError):
#     print 'Some error happened!'
# except (ZeroDivisionError, TypeError, NameError), e:
#     print 'Exception:', e
except:
    print 'Something wrong happened...'
else:
    print 'Ah... It went as planned.'
finally:
    print 'Cleaning up.'
