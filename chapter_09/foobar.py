#!/usr/bin/env python -u


class FooBar(object):
    def __init__(self, value=42):
        self.somevar = value

    def __del__(self):
        print 'I am done. Byebye world! (val=%s)' % str(self.somevar)


f = FooBar()
print f.somevar

f2 = FooBar('This is a constructor argument.')
print f2.somevar
