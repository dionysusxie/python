#!/usr/bin/env python -u

import sys
import os
import hello
import hello2
import drawing
import drawing.colors
from drawing import shapes
import webbrowser


hello.hello()
print(hello.name)

print
hello2.hello()
print(hello2.name)

print
print('PI = ' + str(drawing.PI))


print

# sys.argv
print('sys.argv:')
for index, arg in enumerate(sys.argv):
    print('  ' + str(index) + ': ' + arg)

# sys.modules
print('\nsys.modules:')
for m in sys.modules:
    print('  ' + m + '\n    ' + str(sys.modules[m]) + '\n')


#
# os
#

print

environs = ['PYTHONPATH', 'PATH', 'xxx', 'USER']
for env in environs:
    try:
        print(env + ' = ' + os.environ[env])
    except KeyError as e:
        print(env + ' = NOT FOUND!')

print('os.pathsep = ' + os.pathsep)
print('os.linesep = ' + os.linesep + '#')

print('\npwd:')
os.system('pwd')

print('\nls:')
os.system('ls')


#
# webbrowser
#

# webbrowser.open('http://www.python.org', True, True)


