from pygame.math import Vector2
from constants import *
from parameters import params

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

        # account for current motion
        velocity += + self.currentFlight()

        # add any forces from the edge of the screen
        if(self.flock.world.edgeBehavior == EDGE_RETURN):
            velocity += self.stayInBox(self.flock.world.width,self.flock.world.height)

        nearbyBirds = self.flock.findBirdsInView(self.pos,self.velocity,params.fov,params.birdVisibility)
        self.gravity = None
        if(len(nearbyBirds) > 0):
            # add forces attracting to nearby birds
            velocity += self.flyTowardsToNearbyBirds(nearbyBirds)
            # add forces repelling from birds that are too close
            velocity += self.stayAway(nearbyBirds)
            # add forces aligning with other birds
            velocity += self.fitIn(nearbyBirds)

        nearbyRepulsors = self.flock.repulsors
        velocity += self.stayAwayFromRepulsors(nearbyRepulsors)
        
        velocity = self.limitSpeed(velocity)

        if timeDelta:
            self.velocity = velocity

        delta = velocity * timeDelta        
        self.newPos = self.pos + delta
        if(self.flock.world.edgeBehavior == EDGE_WRAP):
            self.newPos,self.didWrap = wrap(self.newPos,self.flock.world.width,self.flock.world.height)
            if self.didWrap:
                self.tails.append(None)
        else:
            self.didWrap = False

    def currentFlight(self):
        return self.velocity

    def stayInBox(self,width,height):
        b = params.boxMagnetism
        margin = EDGE_MARGIN
        delta = Vector2(0,0)
        if(self.pos.x < margin):
            delta.x += b
        elif self.pos.x > width-margin:
            delta.x -= b
        if self.pos.y < margin:
            delta.y += b
        elif self.pos.y > height-margin:
            delta.y -= b
        return delta

    def stayAway(self,birds):
        delta = Vector2(0,0)
        tooClose2 = params.tooClose * params.tooClose
        for aBird in birds:
            if (aBird.pos - self.pos).length_squared() < tooClose2:
                delta -= (aBird.pos - self.pos)
        return delta

    def stayAwayFromRepulsors(self,repulsors):
        delta = Vector2(0,0)
        tooClose2 = params.tooClose * params.tooClose
        for aRepulsor in repulsors:
            l2 = (aRepulsor.pos - self.pos).length_squared()
            r2 = aRepulsor.radius*aRepulsor.radius
            if l2 < r2:
                r = (aRepulsor.pos - self.pos).length() / aRepulsor.radius

                force = (self.pos - aRepulsor.pos).normalize() * (1/(r*r)) * params.repulsionStrength
                delta += force
        # if delta.length() > 0:
        #     print(f"repulsion force is {delta.length()}")
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
    
    def limitSpeed(self,velocity):
        max = params.birdMaxSpeed
        min = params.birdMinSpeed
        if velocity.length_squared() > (max*max):
            velocity.scale_to_length(max)
        elif velocity.length_squared() < (min*min):
            velocity.scale_to_length(min)
        return velocity
    
    def updatePosition(self):
        self.tails.append(self.newPos)
        if len(self.tails) > TAIL_LENGTH:
            self.tails.pop(0)

        self.pos = self.newPos
        self.newPos = None
