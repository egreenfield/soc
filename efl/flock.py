from dataclasses import dataclass
from grid_partition import GridPartition
from diagnostics import Diagnostics
from bird import Bird
from pygame.math import Vector2
import random
from constants import *
from parameters import params
from list_partition import ListPartition
import numpy as np

#####-----------------------------------------------------------------------------------------------------------------------------
#### Flock
#####-----------------------------------------------------------------------------------------------------------------------------

@dataclass
class Repulsor:
    pos:Vector2
    radius:float = DEFAULT_REPULSOR_RADIUS
    def __init__(self,pos):
        self.pos = Vector2(pos)

class Flock:
    birds:list[Bird]
    repulsors:list[Repulsor]
    partition:ListPartition
    world:any = None
    birdCount:int = 0
    birdData:np.array
    nextBirdData:np.array
    def __init__(self,world):
        self.world = world
        self.clear()
        Diagnostics.setDiagnostic("bird count",lambda : f"{len(self.birds)} birds")
        pass

    def clear(self):
        self.repulsors = []
        self.clearBirds()

    def clearBirds(self):
        self.birds = []
        self.birdCount = 0
        self.birdData = np.zeros((0,8),dtype=np.float64)
        self.nextBirdData = np.zeros((0,8),dtype=np.float64)
        self.partition = GridPartition()

    def killBird(self):
        self.birds.pop()

    def setBirdCount(self,newCount:int):
        delta = newCount - self.birdCount
        if(newCount > self.birdCount):
            newData = np.zeros((newCount, 8), dtype=np.float64)
            self.birdData = np.vstack((self.birdData,newData))
            self.nextBirdData = np.vstack((self.nextBirdData,np.zeros((newCount, 8), dtype=np.float64)))
            for i in range(self.birdCount,newCount):
                self.createRandomBirdAt(i)            
        else:
            self.birdData = self.birdData[:newCount]
            self.birds = self.birds[:newCount]
            #TODO remove from partition
        self.birdCount = newCount

        
    def createRandomBirdAt(self,index):
        newBird = Bird(self,
        pos=Vector2(self.world.width*random.random(),self.world.height*random.random()),
        heading=random.random()*360,
        speed=random.random() * (params.birdMaxSpeed-params.birdMinSpeed) + params.birdMinSpeed,
        index=index 
        )
        self.birds.append(newBird)
        self.partition.register(newBird)

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
    def findBarrierAtPoint(self,pos:Vector2):
        for aRep in self.repulsors:
            if (aRep.pos - pos).length_squared() < MOUSE_HIT_DISTANCE*MOUSE_HIT_DISTANCE:
                return aRep
        return None

    def update(self,delta):
        if delta == 0: 
            return
        for aBird in self.birds:
            aBird.calculateNewPosition(delta)
        for aBird in self.birds:
            newPos = aBird.updatePosition()   
            self.partition.set(aBird,newPos)


    def findBirdsNearby(self,pos:Vector2,maxDistance:float,skip=None):
        return self.partition.findInCircle(pos,maxDistance,skip)

    def findBirdsInView(self,pos:Vector2,dir:Vector2,fovDeg:float,radius:float,skip=None):
        return self.partition.findInCone(pos,dir,fovDeg,radius,skip)
