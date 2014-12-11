#!/usr/bin/env python

import math

x = 2

if x < 5 or (x > 10 and x < 20):
  print "The value is OK."

if x < 5 or 10 < x < 20:
  print "The value is OK."

for i in [1, 2, 3, 4, 5]:
  print "This is iteration number", i

x = 10
while x >= 0:
  print "x is still not negative:", x
  x = x - 1

for value in range(5):
  print value

x = input("Please enter a number: ")
print "The square of that number is", x * x

# list
x = ['i', 'am', 'xie', 'liang']
print "This list is ", x
print "Length of list x is:", len(x)
print x[0:3]
print x[-1]

# dictionary
phone = {
    'Alice': 23452532,
    'Boris': 252336,
    'Clarice': 2352525,
    'Doris': 23624642
}
person = {
    'first name': 'Robin',
    'last name': 'Hood',
    'occupation': 'Scoundrel'
}
print person['first name'], person['last name']


#
# function
#

def square(x):
    return x * x

s = 2
print 'Square of', s, 'is:', square(s)
print 's =', s


def change_list(x):
    x[1] = 4

y = [1, 2, 3]
print 'list of y :', y
change_list(y)
print 'list of y :', y


#
# logic
#

print
print '##### logic:'
logic_test_list = [False, 0, '', ' ', [], {}, None, 123]
for t in logic_test_list:
  if (t):
    print t, 'is true!'
  else:
    print t, 'is false!'


#
# class Basket
#

class Basket:
  def __init__(self, contents = []):
    self.contents = contents[:]

  def add(self, element):
    self.contents.append(element)

  def __str__(self):
    result = 'Contains:'
    for ele in self.contents:
      result = result + ' ' + repr(ele)
    return result


my_age = 2
def test():
  my_age = 18
  print 'test(): my_age = ' + str(my_age)


#
# main()
#

def main():
  print '##### This is main() #####'

  test()
  print 'my age: ' + str(my_age)

  init_fruits = ['apple', 'orange']
  basket_a = Basket(init_fruits)
  basket_b = Basket(init_fruits)
  basket_a.add('watermelon')
  print basket_a
  print basket_b

  print 'sqrt of 4 is:', math.sqrt(4)

if __name__ == '__main__':
  main()

