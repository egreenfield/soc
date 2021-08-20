from dataclasses import dataclass
from bird import Bird
from pygame.math import Vector2
import random
from constants import *
from parameters import params

#####-----------------------------------------------------------------------------------------------------------------------------
#### Flock
#####-----------------------------------------------------------------------------------------------------------------------------

@dataclass
class Repulsor:
    pos:Vector2

class Flock:
    birds:list[Bird]
    repulsors:list[Repulsor]
    world:any = None
    def __init__(self,world):
        self.birds = []
        self.repulsors = []
        self.world = world
        pass
    def clear(self):
        self.birds = []

    def killBird(self):
        self.birds.pop()

    def createRandomBird(self):
        newBird = Bird(self,
        pos=Vector2(self.world.width*random.random(),self.world.height*random.random()),
        heading=random.random()*360,

        speed=random.random() * (params.birdMaxSpeed-params.birdMinSpeed) + params.birdMinSpeed
        )
        self.birds.append(newBird)

    def addRepulsor(self,r):
        try:
            self.repulsors.index(r)
        except:
            self.repulsors.append(r)

    def removeRepulsor(self,r):
        try:
            self.repulsors.remove(r)
        except:
            pass
        
    def update(self,delta):
        if delta == 0: 
            return
        for aBird in self.birds:
            aBird.calculateNewPosition(delta)
        for aBird in self.birds:
            aBird.updatePosition()    

    def findBirdsNearby(self,pos:Vector2,maxDistance:float,minDistance:float=0):
        nearbyBirds = []
        min2 = minDistance * minDistance
        max2 = maxDistance*maxDistance
        for aBird in self.birds:
            delta = aBird.pos - pos
            d2 = delta.length_squared()
            if(d2 > min2 and d2 < max2):
                nearbyBirds.append(aBird)
        return nearbyBirds

    def findBirdsInView(self,pos:Vector2,dir:Vector2,fovDeg:float,maxDistance:float,minDistance:float=0):
        nearbyBirds = []
        min2 = minDistance * minDistance
        max2 = maxDistance*maxDistance
        for aBird in self.birds:
            delta = aBird.pos - pos
            d2 = delta.length_squared()
            if(d2 <= min2 or d2 >= max2):
                continue
            a = dir.angle_to(delta)
            if abs(a) > fovDeg/2:
                continue
            nearbyBirds.append(aBird)
        return nearbyBirds
