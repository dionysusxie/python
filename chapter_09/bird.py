#!/usr/bin/env python -u


class Bird(object):
    def __init__(self):
        self.hungry = True

    def eat(self):
        if self.hungry:
            print 'Aaaah... Delicious!'
            self.hungry = False
        else:
            print 'No, thanks! I am full.'

    def fly(self):
        self._fly()

    def _fly(self):
        print "I can't fly!"

b = Bird()
b.eat()
b.eat()
b.fly()


class SongBird(Bird):
    def __init__(self):
        super(SongBird, self).__init__()
        # or:
        # Bird.__init__(self)

        self.sound = 'Squawk'

    def sing(self):
        print self.sound

    def _fly(self):
        print "I am flying..."

print
sb = SongBird()
sb.sing()
sb.eat()
sb.fly()
