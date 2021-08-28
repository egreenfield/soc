from id import ID
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

I_PX = 0
I_PY = 1
I_VX = 2
I_VY = 3
I_NEIGHBORCOUNT = 4

class Bird:
    newPos:Vector2
    flock:any
    tails:list[Vector2]
    index:int = 0

    @property
    def pos(self):
        data = self.flock.birdData[self.index]
        return Vector2(data[I_PX],data[I_PY])
    @pos.setter
    def pos(self,value):
        data = self.flock.birdData[self.index]
        data[I_PX] = value.x
        data[I_PY] = value.y

    
    @property
    def velocity(self):
        data = self.flock.birdData[self.index]
        return Vector2(data[I_VX],data[I_VY])
    @velocity.setter
    def velocity(self,value):
        data = self.flock.birdData[self.index]
        data[I_VX] = value.x
        data[I_VY] = value.y

    @property
    def gravity(self):
        data = self.flock.birdData[self.index]
        return Vector2(data[I_NEIGHBORCOUNT],data[I_NEIGHBORCOUNT+1])

    @gravity.setter
    def gravity(self,value):
        data = self.flock.birdData[self.index]
        data[I_NEIGHBORCOUNT] = value.x
        data[I_NEIGHBORCOUNT+1] = value.y


    def __init__(self,flock,pos,heading,speed,index): 
        self.flock = flock
        self.index = index
        self.tails = []
        self.id = ID.allocate()
        self.pos = pos
        self.velocity = Vector2(speed,0).rotate(heading)

        
    def __hash__(self) -> int:
        return self.id

    def copyToData(self):
        d = self.data
        d[I_PX] = self.pos.x
        d[I_PY] = self.pos.y
        d[I_VX] = self.velocity.x
        d[I_VY] = self.velocity.y

    def calculateNewPosition(self,timeDelta):
        timeDelta = timeDelta / 1000.0
        velocity = Vector2(0,0)

        # account for current motion
        velocity += + self.currentFlight()

        # add any forces from the edge of the screen
        if(self.flock.world.edgeBehavior == EDGE_RETURN):
            velocity += self.stayInBox(self.flock.world.width,self.flock.world.height)

        nearbyBirds = self.flock.findBirdsInView(self.pos,self.velocity,params.fov,params.birdVisibility,self)
        #nearbyBirds = self.flock.findBirdsNearby(self.pos,params.birdVisibility,self)
        self.gravity = Vector2(0,0)
        if (len(nearbyBirds) > 0):
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
            delta.x += (margin - self.pos.x)*b
        elif self.pos.x > width-margin:
            delta.x -= (self.pos.x-(width-margin))*b
        if self.pos.y < margin:
            delta.y += (margin - self.pos.y)*b
        elif self.pos.y > height-margin:
            delta.y -= (self.pos.y-(height-margin))*b
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
        return self.pos
