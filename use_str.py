#!/usr/bin/env python -u

import math
import string
from string import Template

print 'Pi with three decimals: %.3f' % math.pi

s = Template('$x, glorious $x!')
print s.substitute(x = 'China')

s = Template("It's ${x}tastic!")
print s.substitute(x = 'slurm')

s = Template('Make $$ selling $x!')
print s.substitute(x = 'slurm')

s = Template('A $thing must never $action.')
d = {
     'thing':   'gentleman',
     'action':  'show his socks'
}
print s.substitute(d)

print

print '%s plus %s equals %s' % (1, 1, 2)

print 'dec: %d, oct: %o, hex: %x %X, e: %e %E' % (10, 10, 10, 10, 10.0, 10.0)

# width
print
print 'PI:%10.2f' % math.pi
print 'PI:%010.2f' % math.pi
print 'PI:%-10.2f#' % math.pi
print 'PI:%1.2f#' % math.pi
print 'My name:%10s' % 'DioXie'
print 'My name:%-10s#' % 'DioXie'
print 'My name:%10.4s#' % 'DioXie'
print 'My name:%1.4s#' % 'DioXie'
print '%.*s' % (5, 'Guido van Rossum')
print '%+5d' % 10 + '\n%+5d' % -10

# string class Variable
print string.digits
print string.ascii_letters
print string.ascii_lowercase
print string.ascii_uppercase
print string.punctuation
print string.printable

# string.join()
print
seq = ['1', '2', '3']
print ' + '.join(seq) + ' = ' + str(sum([1,2,3]))
dirs = '', 'usr', 'bin', 'env'
print '/'.join(dirs)
print 'C:' + '\\'.join(dirs)

# string.split()
print
print '1+2+3+4+5'.split('+')
print '/usr/bin/env'.split('/')
print 'Using the \t default\n.'.split()

# string.lower()
print
print 'Trondheim Hammer Dance'.lower()

# string.replace()
print 'This is a test'.replace('is', 'eez')

# string.strip(s, chars)
print '  \t I am Xieliang.  \n\t'.strip() + '#'
print '*** SPAM * for * everyone!!! ***'.strip(' *!') + '#'

# string.translate(s, table, deletions)
print
trans_table = string.maketrans('cs', 'kz')
print 'translate table: ', trans_table[97:123]
origin_str = 'this is a incredible test'
print 'origin str     : ' + origin_str
print 'translated str : ' + origin_str.translate(trans_table)


