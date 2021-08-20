from bird import Bird
from pygame.math import Vector2
import random
from constants import *

#####-----------------------------------------------------------------------------------------------------------------------------
#### Flock
#####-----------------------------------------------------------------------------------------------------------------------------

class Flock:
    birds:list[Bird]
    world:any = None
    def __init__(self,world):
        self.birds = []
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
