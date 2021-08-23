
from pygame import Vector2
from flock import Flock, Repulsor
from constants import *

#####-----------------------------------------------------------------------------------------------------------------------------
#### World
#####-----------------------------------------------------------------------------------------------------------------------------
class World:
    playerPosition = None
    flock:Flock
    width:int
    height:int
    runStyle:int
    drawDiagnostics:bool = False
    drawTails:bool = False
    edgeBehavior:int = EDGE_DEFAULT_BEHAVIOR
    mouse:Repulsor
    
    def __init__(self,w:int,h:int):
        self.width = w
        self.height = h
        self.flock = Flock(self)
        self.runStyle = STARTING_RUNSTYLE
        self.mouse = Repulsor(pos=Vector2())

    def reset(self):
        self.flock.clear()
        self.resetBirds()
    def resetBirds(self):
        self.flock.clearBirds()
        self.flock.setBirdCount(STARTING_BIRD_COUNT)
    def addBirds(self,count:int):
        self.flock.setBirdCount(self.flock.birdCount+count)
    def removeBirds(self,count:int):
        self.flock.setBirdCount(self.flock.birdCount-count)

