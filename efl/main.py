from dataclasses import dataclass
from typing import Tuple
import pygame
from pygame.locals import *
from pygame.math import Vector2
import random
import math
from pygame import Surface

#####-----------------------------------------------------------------------------------------------------------------------------
#### Playback state
#####-----------------------------------------------------------------------------------------------------------------------------

CONTINUOUS = 0
STOP = 1
STEP = 2
STARTING_RUNSTYLE = CONTINUOUS

EDGE_WRAP = 0
EDGE_RETURN = 1
EDGE_BEHAVIOR = EDGE_WRAP

WORLD_WIDTH     = 1800
WORLD_HEIGHT    = 900
STARTING_BIRD_COUNT = 200
#####-----------------------------------------------------------------------------------------------------------------------------
#### Simulation constants
#####-----------------------------------------------------------------------------------------------------------------------------

BIRD_LENGTH = 10

class Constants:
    birdMaxSpeed:float 
    birdMinSpeed:float 
    birdVisibility:float
    boxMagnetism:float 
    tooClose:float 
    individuality:float
    gravitationalStrength:float


const = Constants()

class Parameter:
    name:str
    key:str
    code:int
    min:float
    max:float
    value:float

    params = {}

    def setValue(self,newValue:float):        
        self.value = newValue
        setattr(const,self.name,newValue)
    
    def adjustValue(self,delta:float):
        v = self.value + delta
        if v > self.max:
            v = self.max
        if v < self.min:
            v = self.min
        self.value = v
        setattr(const,self.name,self.value)

    def mapValue(self,pct:float):
        return self.min + (self.max-self.min)*pct

    def mapRelativeValue(self,pct:float):
        return (self.max-self.min)*pct

    @classmethod
    def get(self,code:int):
        if code in self.params:
            return self.params[code]
        return None

    @classmethod
    def add(self,**kwargs):
        p = Parameter()
        for aKey in kwargs:
            setattr(p,aKey,kwargs[aKey])
        self.params[kwargs['code']] = p #Parameter(**kwargs)
        setattr(const,kwargs['name'],kwargs['value'])

    @classmethod
    def printHelp(self):
        result = ""
        for aParam in self.params.values():
            result += f"{aParam.key}:{aParam.name} ({aParam.value})\n"
        print(result)

Parameter.add(name='birdMaxSpeed',code=K_m,key="m",min=20,max=1000,value=350)
Parameter.add(name='birdMinSpeed',code=K_n,key="n",min=20,max=1000,value=100)
Parameter.add(name='birdVisibility',code=K_v,key="v",min=1,max=200,value=80)
Parameter.add(name='boxMagnetism',code=K_x,key="x",min=1,max=200,value=10)
Parameter.add(name='tooClose',code=K_c,key="m",min=1,max=100,value=20)
Parameter.add(name='individuality',code=K_i,key="i",min=1,max=30,value=5)
Parameter.add(name='gravitationalStrength',code=K_g,key="g",min=.01,max=1,value=.05)


    
#####-----------------------------------------------------------------------------------------------------------------------------
#### Graphics constants
#####-----------------------------------------------------------------------------------------------------------------------------
TAIL_LENGTH = 20

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

        nearbyBirds = self.flock.findBirdsNearby(self.pos,const.birdVisibility)        
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
        b = const.boxMagnetism
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
        tooClose2 = const.tooClose * const.tooClose
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
        return (delta-self.pos) * const.gravitationalStrength
    
    def fitIn(self,nearbyBirds):
        delta = Vector2(0,0)
        for aBird in nearbyBirds:
            delta += aBird.velocity
        delta /= len(nearbyBirds)
        return (delta - self.velocity) / const.individuality
    
    def limitSpeed(self):
        max = const.birdMaxSpeed
        min = const.birdMinSpeed
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

        speed=random.random() * (const.birdMaxSpeed-const.birdMinSpeed) + const.birdMinSpeed
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
    activeParameter:Parameter = None
    
    
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



#####-----------------------------------------------------------------------------------------------------------------------------
#### Graphics
#####-----------------------------------------------------------------------------------------------------------------------------
class Graphics:
    world:World

    def __init__(self,world:World):
        self.world = world
        self.screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
        self.birdSurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
        self.tailSurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
        self.debugSurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)

    def draw(self):
        self.screen.fill((250,250,250))    
        self.birdSurface.fill((0,0,0,0))    
        self.tailSurface.fill((0,0,0,0))    
        self.debugSurface.fill((0,0,0,0))    
        self.drawFlock()
        self.screen.blit(self.tailSurface,(0,0))
        self.screen.blit(self.debugSurface,(0,0))
        self.screen.blit(self.birdSurface,(0,0))


    def drawFlock(self):
        f = self.world.flock
        for aBird in f.birds:
            self.drawBird(aBird)
    def drawTails(self,bird:Bird):
        start = 0
        try:
            while True:
                end = bird.tails.index(None,start)
                if(end-start >= 2):
                    pygame.draw.lines(self.tailSurface,(0,0,150,50),False,bird.tails[start:end])
                start = end+1
        except:            
            pass
        if(len(bird.tails)-start > 2):
            pygame.draw.lines(self.tailSurface,(0,0,150,50),False,bird.tails[start:])

    def drawDiagnostics(self,bird:Bird):
        if(bird.gravity != None):
            pygame.draw.circle(self.debugSurface,Color(230,230,255,150),center=bird.pos,radius=const.birdVisibility)
            if(not bird.didWrap):
                pygame.draw.line(self.birdSurface,(0,0,255),bird.pos,bird.gravity,1)
        else:
            pygame.draw.circle(self.debugSurface,Color(255,230,230,150),center=bird.pos,radius=const.birdVisibility)

    def drawBird(self,bird:Bird):
        heading = Vector2(bird.velocity)
        heading.scale_to_length(BIRD_LENGTH)
        if(self.world.drawDiagnostics):
            self.drawDiagnostics(bird)
        pygame.draw.line(self.birdSurface,(255,0,0),bird.pos,bird.pos+heading,2)
        if(self.world.drawTails):
            self.drawTails(bird)


#####-----------------------------------------------------------------------------------------------------------------------------
#### USer Input/Events
#####-----------------------------------------------------------------------------------------------------------------------------
def adjustParameter(world:World,rel):
    if world.activeParameter == None:
        return

    pct = rel[0] / world.width
    delta = world.activeParameter.mapRelativeValue(pct)
    #world.activeParameter.setValue(newValue)    
    world.activeParameter.adjustValue(delta)    
    print(f"setting {world.activeParameter.name} to {world.activeParameter.value}")

    
def processEvents(world:World):
    for event in pygame.event.get():
        if event.type == QUIT:
            return True
        if event.type == KEYDOWN:
            param = Parameter.get(event.key)
            if(param != None):
                world.activeParameter = param
                print(f"controlling {param.name}")
            if event.key == K_RETURN:
                world.runStyle = STEP
            elif event.key == K_SPACE:
                world.runStyle = CONTINUOUS
            elif event.key == K_r:
                world.reset()
            elif event.key == K_d:
                world.drawDiagnostics = not world.drawDiagnostics
            elif event.key == K_UP:
                world.addBirds(10)
            elif event.key == K_DOWN:
                world.removeBirds(10)
            elif event.key == K_e:
                world.edgeBehavior = 1 - world.edgeBehavior
            elif event.key == K_t:
                world.drawTails = not world.drawTails
            elif event.key == K_QUESTION or event.key == K_SLASH:
                Parameter.printHelp()
        if event.type == KEYUP:
            world.activeParameter = None
        if event.type == MOUSEMOTION:
            if(event.buttons[0]):
                adjustParameter(world,event.rel)


    return False

def updateWorld(world,delta):
    # this is a good place to make updates to the game world that 
    # doesn't happen in response to an event.  Like, say, if a ball is flying through space
    # then you need to update its position because time has passed.
    world.flock.update(delta)


#---------------------------------------------------------------------------
#
# Drawing
#
#---------------------------------------------------------------------------
def draw(world,graphics):
    # this is where you draw the screen based on what the current state of your world is.
    graphics.draw()
    pygame.display.flip()


#---------------------------------------------------------------------------
#
# The main program
#
#---------------------------------------------------------------------------

def runLoop(world,graphics):
    # this is what's called the 'main loop' of the program.  It's basically 
    # how all programs work...apps, games, etc.  Sometimes you write it yourself (like we do here),
    # and sometimes a library handles it for you.  Regardless, the basics are the same...
    # 1) check to see if anything has happened
    # 2) do periodic updates and maintenance
    # 3) update the screen 
    # 4) repeat until it's time to quit
    clock = pygame.time.Clock()

    while 1:
        if(world.runStyle == CONTINUOUS):
            delta = clock.tick(30)
        elif world.runStyle == STEP:
            delta = 100
            world.runStyle = STOP
        else:
            delta = 0
        shouldQuit = processEvents(world)
        if(shouldQuit):
            return
        updateWorld(world,delta)
        draw(world,graphics)


#####-----------------------------------------------------------------------------------------------------------------------------
#### Main program
#####-----------------------------------------------------------------------------------------------------------------------------

def main():
    pygame.init()
    pygame.display.set_caption('Boids')

    # initialize the world
    world:World = World(WORLD_WIDTH,WORLD_HEIGHT)

    # initialize graphics
    graphics = Graphics(world)

    world.reset()

    draw(world,graphics)

    # Event loop
    runLoop(world,graphics)



if __name__ == '__main__': main()
