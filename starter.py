import gamestate as gs
import sys
import math

def closest(ent, entities):
    return min(entities, key=lambda x: dist(ent, x))

def dist(entity, other):
    # note this does not take wrap around into account
    return magnitude((entity.x - other.x), (entity.y - other.y))

def getEntityAngle(entity, other):
    # gives the angle of the vector from entity to other
    x = other.x - entity.x
    y = other.y - entity.y
    return getAngle(x,y)

def getAngle(x, y):
    # wrt to the positive x axis (but clockwise, counter intuitive but coords are upside down)
    # e.g.
    #               315
    #             .
    #           .
    #  180 . . x . . 0
    #           .
    #             .
    #               45
    return (math.degrees(math.atan2(y, x)) + 360) % 360
    
def magnitude(x, y):
    return ((x)**2 + (y)**2)**(1.0/2)



r = gs.Response()
state = gs.GameState()

while True:
    # get game state
    state.read()

    if(state.asteroids):
        close = closest(state.ship, state.asteroids)
        angle = getEntityAngle(state.ship, close)
        thresh = 15
        if(state.ship.angle > angle):
            r.set_ccw()
        elif(state.ship.angle < angle):
            r.set_cw()

        # fire if close to on target
        r.set_fire(abs(state.ship.angle - angle) < thresh)

        distance = dist(state.ship, close)

        # are we flying backwards?
        backwards = abs(getAngle(state.ship.dx, state.ship.dy) - state.ship.angle) > 150

        velocity = magnitude(state.ship.dx, state.ship.dy)

        if(abs(state.ship.angle - angle) < thresh and distance > 400 and velocity < 5):
            # if closest object is far away boost to it
            r.set_thrust(True)
        elif (distance > 100 and backwards):
            # slow down if possible
            r.set_thrust(True)
        else:
            r.set_thrust(False)

    # send command
    r.send()
