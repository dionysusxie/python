#!/usr/bin/env python -u
from logging import Filter

__metaclass__ = type

class Filter:

    def __init__(self):
        self.blocked = []

    def filter(self, sequence):
        return [x for x in sequence if x not in self.blocked]


class SPAM_Filter(Filter):
    def __init__(self):
        self.blocked = ['SPAM']


f = Filter()
print f.filter([1, 2, 3])

s = SPAM_Filter()
s_list = ['SPAM', 'SPAM', 'ONE', 'spam']
print 'Origin list:', s_list
print 'List after filtering with SPAM:', s.filter(s_list)


# issubclass()
if issubclass(SPAM_Filter, Filter):
    print 'SPAM_Filter is a subclass of Filter.'
else:
    print 'SPAM_Filter is NOT a subclass of Filter.'

# __bases__
print 'Superclasses of SPAM_Filter: ' + str(SPAM_Filter.__bases__)


#
# isinstance()
#

def isinstanceTest(obj, class_tested):
    if isinstance(obj, class_tested):
        print 'Tested obj is a instance of class ' + str(class_tested)
    else:
        print 'Tested obj is NOT a instance of class ' + str(class_tested)

isinstanceTest(s, Filter)
isinstanceTest(s, SPAM_Filter)

