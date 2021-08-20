
from flock import Flock
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
    edgeBehavior:int = EDGE_BEHAVIOR
    
    
    def __init__(self,w:int,h:int):
        self.width = w
        self.height = h
        self.flock = Flock(self)
        self.runStyle = STARTING_RUNSTYLE


    def reset(self):
        self.flock.clear()
        for i in range(STARTING_BIRD_COUNT):
            self.flock.createRandomBird()
    def addBirds(self,count:int):
        for i in range(count):
            self.flock.createRandomBird()
    def removeBirds(self,count:int):
        for i in range(count):
            self.flock.killBird()

