#!/usr/bin/env python -u

import fileinput

for line in fileinput.input(inplace=True, backup='.bak'):
    line = line.rstrip()
    num = fileinput.lineno()
    print '%-75s # %2i' % (line, num)

fileinput.close()
