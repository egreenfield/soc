from cl_flock import CLFlock
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

BIRD_DATUM_COUNT = 8
REPULSOR_DATUM_COUNT = 8


kObjectPX = 0
kObjectPY = 1


@dataclass
class Repulsor:
    pos:Vector2
    radius:float = DEFAULT_REPULSOR_RADIUS
    
    def __init__(self,pos,flock,index):
        self.flock = flock
        self.index = index
        self.pos = Vector2(pos)

    @property
    def pos(self):
        data = self.flock.repulsorData[self.index]
        return Vector2(data[kObjectPX],data[kObjectPY])

    @pos.setter
    def pos(self,value):
        data = self.flock.repulsorData[self.index]
        data[kObjectPX] = value.x
        data[kObjectPY] = value.y


class Flock:
    birds:list[Bird]
    repulsors:list[Repulsor]
    partition:ListPartition
    world:any = None
    birdCount:int = 0
    birdData:np.array    
    nextBirdData:np.array
    repulsorData:np.array
    
    clRenderer:CLFlock = None
    def __init__(self,world):
        self.world = world
        self.clRenderer = CLFlock(world)        
        self.clear()
        Diagnostics.setDiagnostic("bird count",lambda : f"{len(self.birds)} birds")
        pass

    def clear(self):
        self.repulsors = []
        self.clearBirds()

    def clearBirds(self):
        self.birds = []
        self.birdCount = 0
        self.birdData = np.zeros((0,BIRD_DATUM_COUNT),dtype=np.float32)
        self.nextBirdData = np.zeros((0,BIRD_DATUM_COUNT),dtype=np.float32)
        self.repulsorData = np.zeros((0,REPULSOR_DATUM_COUNT),dtype=np.float32)
        self.partition = GridPartition()

    def killBird(self):
        self.birds.pop()

    def resizeBuffer(self,buffer,oldCount:int,newCount:int,datumCount:int):
        delta = newCount - oldCount
        if(newCount > oldCount):
            newData = np.zeros((delta, datumCount), dtype=np.float32)
            return np.vstack((buffer,newData))
        else:
            return buffer[:newCount]


    def setBirdCount(self,newCount:int):
        self.birdData = self.resizeBuffer(self.birdData,self.birdCount,newCount,BIRD_DATUM_COUNT);
        self.nextBirdData = self.resizeBuffer(self.nextBirdData,self.birdCount,newCount,BIRD_DATUM_COUNT);
        delta = newCount - self.birdCount
        if(newCount > self.birdCount):
            for i in range(self.birdCount,newCount):
                self.createRandomBirdAt(i)            
        else:
            self.birds = self.birds[:newCount]
        self.birdCount = newCount            
        self.updateBufferSizes()

        
    def createRandomBirdAt(self,index):
        newBird = Bird(self,
        pos=Vector2(self.world.width*random.random(),self.world.height*random.random()),
        heading=random.random()*360,
        speed=random.random() * (params.birdMaxSpeed-params.birdMinSpeed) + params.birdMinSpeed,
        index=index 
        )
        self.birds.append(newBird)
        self.partition.register(newBird)

    def addRepulsor(self,p):
        currentRepulstorCount = len(self.repulsors)
        self.repulsorData = self.resizeBuffer(self.repulsorData,currentRepulstorCount,currentRepulstorCount+1,REPULSOR_DATUM_COUNT)
        r = Repulsor(p,self,currentRepulstorCount)
        self.repulsors.append(r)
        self.updateBufferSizes()
        return r

    def removeRepulsor(self,r:Repulsor):
        currentRepulstorCount = len(self.repulsors)
        if (currentRepulstorCount >= 2):
            lastRepulsor = self.repulsors[currentRepulstorCount-1]
            i = r.index
            self.repulsorData[i] = self.repulsorData[lastRepulsor.index]
            self.repulsors[i] = lastRepulsor
            lastRepulsor.index = i
            self.repulsorData = self.resizeBuffer(self.repulsorData,currentRepulstorCount,currentRepulstorCount-1,REPULSOR_DATUM_COUNT)

    def findBarrierAtPoint(self,pos:Vector2):
        for aRep in self.repulsors:
            if (aRep.pos - pos).length_squared() < MOUSE_HIT_DISTANCE*MOUSE_HIT_DISTANCE:
                return aRep
        return None

    def update(self,delta):
        if delta == 0: 
            return
        # for aBird in self.birds:
        #     aBird.calculateNewPosition(delta)

        self.clRenderer.setBuffers(self.birdData,self.nextBirdData,self.repulsorData)
        self.clRenderer.runUpdate(delta)
        tmp = self.birdData
        self.birdData = self.nextBirdData
        self.nextBirdData = self.birdData

        # for aBird in self.birds:
        #     newPos = aBird.updatePosition()   
        #     self.partition.set(aBird,newPos)

    def updateBufferSizes(self):
        self.clRenderer.setBufferSize(self.birdCount,self.birdData.nbytes,len(self.repulsors),self.repulsorData.nbytes)



    def findBirdsNearby(self,pos:Vector2,maxDistance:float,skip=None):
        return self.partition.findInCircle(pos,maxDistance,skip)

    def findBirdsInView(self,pos:Vector2,dir:Vector2,fovDeg:float,radius:float,skip=None):
        return self.partition.findInCone(pos,dir,fovDeg,radius,skip)
