import sys

class Entity(object):
    def __init__(self, pos, vel):
        self.x, self.y = [float(val) for val in pos[1:-1].split(',')]
        self.dx, self.dy = [float(val) for val in vel[1:-1].split(',')]


class Ship(Entity):
    def __init__(self, pos, vel, angle, shield):
        self.angle = float(angle)
        self.shield = int(shield)
        super(Ship, self).__init__(pos, vel)

class Asteroid(Entity):
    def __init__(self, pos, vel, scale):
        self.scale = float(scale)
        super(Asteroid, self).__init__(pos, vel)

class GameState():
    def __init__(self, fd=sys.stdin):
        self.asteroids = []
        self.bullets = []
        self.alien = None
        self.ship = None
        try:
            self.height, self.width = fd.readline().split()
        except Exception as e:
            sys.stderr.write("Getting global settings failed\n")
            quit()
        self.height = int(self.height)
        self.width = int(self.width)

    def read(self, fd=sys.stdin):
        try:
            try:
                num = int(fd.readline())
            except ValueError:
                sys.stderr.write("Malformated or missing input\n")
                quit()

            self.asteroids = []
            self.bullets = []
            self.alien = None
            self.ship = None
            for i in range(num):
                words = fd.readline().split()
                if(words[0] == 'asteroid'):
                    self.asteroids.append(Asteroid(*words[1:]))
                elif(words[0] == 'ship'):
                    self.ship = Ship(*words[1:])
                elif(words[0] == 'alien'):
                    self.alien = Entity(*words[1:])
                elif(words[0] == 'bullet'):
                    self.bullets.append(Entity(*words[1:]))
            fd.readline() # "stop"
        except IOError:
            sys.stderr.write("Reading from parent failed\n")
            quit()


class Response():
    def __init__(self):
        self._cw = False
        self._ccw = False
        self._thrust = False
        self._fire = False
    def set_cw(self):
        self._cw = True
        self._ccw = False
    def set_ccw(self):
        self._cw = False
        self._ccw = True
    def set_no_turn(self):
        self._cw = False
        self._ccw = False
    def set_thrust(self, on):
        self._thrust = on
    def set_fire(self, on):
        self._fire = on
    def send(self, fd=sys.stdout):
        turn = "off"
        if self._cw:
            turn = "cw"
        elif self._ccw:
            turn = "ccw"
        thrust = "on" if self._thrust else "off"
        fire = "on" if self._fire else "off"
        try:
            fd.write("%s %s %s\n" % (turn, thrust, fire))
            fd.flush()
        except IOError:
            sys.stderr.write("Communication with parent failed")
            quit()
