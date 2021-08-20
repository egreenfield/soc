from pygame.math import Vector2
from constants import *
#####-----------------------------------------------------------------------------------------------------------------------------
#### utility functions
#####-----------------------------------------------------------------------------------------------------------------------------

def wrap(v,w,h):
    didWrap = False
    if v.x < 0:
        v.x = w + v.x
        didWrap = True
    elif v.x > w:
        v.x = v.x - w
        didWrap = True
    if v.y < 0:
        v.y = h + v.y
        didWrap = True
    elif v.y > h:
        v.y = v.y - h
        didWrap = True
    return (v,didWrap)

#####-----------------------------------------------------------------------------------------------------------------------------
#### Bird
#####-----------------------------------------------------------------------------------------------------------------------------

class Bird:
    pos:Vector2
    newPos:Vector2
    gravity:Vector2 = None
    flock:any
    tails:list[Vector2]
    wrapped:bool = False
    def __init__(self,flock,pos,heading,speed):
        self.pos = pos
        self.velocity = Vector2(speed,0).rotate(heading)
        self.speed = speed
        self.flock = flock
        self.tails = []

    def calculateNewPosition(self,timeDelta):
        timeDelta = timeDelta / 1000.0
        velocity = Vector2(0,0)

        velocity += + self.currentFlight()
        if(self.flock.world.edgeBehavior == EDGE_RETURN):
            velocity += self.stayInBox(self.flock.world.width,self.flock.world.height)

        nearbyBirds = self.flock.findBirdsNearby(self.pos,params.birdVisibility)        
        self.gravity = None
        if(len(nearbyBirds) > 0):
            velocity += self.flyTowardsToNearbyBirds(nearbyBirds)
            velocity += self.stayAway(nearbyBirds)
            velocity += self.fitIn(nearbyBirds)

        self.velocity = velocity
        self.limitSpeed()

        delta = velocity * timeDelta        
        self.newPos = self.pos + delta
        if(self.flock.world.edgeBehavior == EDGE_WRAP):
            self.newPos,self.didWrap = wrap(self.newPos,self.flock.world.width,self.flock.world.height)
            if self.didWrap:
                self.tails.append(None)

    def currentFlight(self):
        return self.velocity

    def stayInBox(self,width,height):
        b = params.boxMagnetism
        delta = Vector2(0,0)
        if(self.pos.x < 0):
            delta.x += b
        elif self.pos.x > width:
            delta.x -= b
        if self.pos.y < 0:
            delta.y += b
        elif self.pos.y > height:
            delta.y -= b
        return delta

    def stayAway(self,birds):
        delta = Vector2(0,0)
        tooClose2 = params.tooClose * params.tooClose
        for aBird in birds:
            if (aBird.pos - self.pos).length_squared() < tooClose2:
                delta -= (aBird.pos - self.pos)
        return delta

    def flyTowardsToNearbyBirds(self,nearbyBirds):
        delta = Vector2(0,0)
        if(len(nearbyBirds) > 0):
            for aBird in nearbyBirds:
                delta = delta + aBird.pos
            delta = delta / len(nearbyBirds)
        self.gravity = delta
        return (delta-self.pos) * params.gravitationalStrength
    
    def fitIn(self,nearbyBirds):
        delta = Vector2(0,0)
        for aBird in nearbyBirds:
            delta += aBird.velocity
        delta /= len(nearbyBirds)
        return (delta - self.velocity) / params.individuality
    
    def limitSpeed(self):
        max = params.birdMaxSpeed
        min = params.birdMinSpeed
        if self.velocity.length_squared() > (max*max):
            self.velocity.scale_to_length(max)
        elif self.velocity.length_squared() < (min*min):
            self.velocity.scale_to_length(min)
    
    def updatePosition(self):
        self.tails.append(self.newPos)
        if len(self.tails) > TAIL_LENGTH:
            self.tails.pop(0)

        self.pos = self.newPos
        self.newPos = None
