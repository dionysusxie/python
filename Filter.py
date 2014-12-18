#!/usr/bin/env python -u

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
print s_list
print s.filter(s_list)
