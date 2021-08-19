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

#####-----------------------------------------------------------------------------------------------------------------------------
#### Simulation constants
#####-----------------------------------------------------------------------------------------------------------------------------

BIRD_MAX_SPEED = 350
BIRD_MIN_SPEED = 100
STARTING_BIRD_COUNT = 200
BIRD_LENGTH = 10
BIRD_VISIBILITY = 80
BOX_MAGNETISM = 100
TOO_CLOSE = 20
INDIVIDUALITY = 5
GRAVITATIONAL_STRENGTH = .05

TOO_CLOSE2 = TOO_CLOSE*TOO_CLOSE

def wrap(v,w,h):
    if v.x < 0:
        v.x = w + v.x
    elif v.x > w:
        v.x = v.x - w
    if v.y < 0:
        v.y = h + v.y
    elif v.y > h:
        v.y = v.y - h
    return v

#####-----------------------------------------------------------------------------------------------------------------------------
#### Bird
#####-----------------------------------------------------------------------------------------------------------------------------

class Bird:
    pos:Vector2
    newPos:Vector2
    gravity:Vector2 = None
    flock:any
    def __init__(self,flock,pos,heading,speed):
        self.pos = pos
        self.velocity = Vector2(speed,0).rotate(heading)
        self.speed = speed
        self.flock = flock

    def calculateNewPosition(self,timeDelta):
        timeDelta = timeDelta / 1000.0
        velocity = Vector2(0,0)

        velocity += + self.currentFlight()
        if(self.flock.world.edgeBehavior == EDGE_RETURN):
            velocity += self.stayInBox(self.flock.world.width,self.flock.world.height)

        nearbyBirds = self.flock.findBirdsNearby(self.pos,BIRD_VISIBILITY)        
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
            self.newPos = wrap(self.newPos,self.flock.world.width,self.flock.world.height)

    def currentFlight(self):
        return self.velocity

    def stayInBox(self,width,height):
        delta = Vector2(0,0)
        if(self.pos.x < 0):
            delta.x += BOX_MAGNETISM
        elif self.pos.x > width:
            delta.x -= BOX_MAGNETISM
        if self.pos.y < 0:
            delta.y += BOX_MAGNETISM
        elif self.pos.y > height:
            delta.y -= BOX_MAGNETISM
        return delta

    def stayAway(self,birds):
        delta = Vector2(0,0)
        for aBird in birds:
            if (aBird.pos - self.pos).length_squared() < TOO_CLOSE2:
                delta -= (aBird.pos - self.pos)
        return delta

    def flyTowardsToNearbyBirds(self,nearbyBirds):
        delta = Vector2(0,0)
        if(len(nearbyBirds) > 0):
            for aBird in nearbyBirds:
                delta = delta + aBird.pos
            delta = delta / len(nearbyBirds)
        self.gravity = delta
        return (delta-self.pos) * GRAVITATIONAL_STRENGTH
    
    def fitIn(self,nearbyBirds):
        delta = Vector2(0,0)
        for aBird in nearbyBirds:
            delta += aBird.velocity
        delta /= len(nearbyBirds)
        return (delta - self.velocity) / INDIVIDUALITY
    
    def limitSpeed(self):
        if self.velocity.length_squared() > (BIRD_MAX_SPEED*BIRD_MAX_SPEED):
            self.velocity.scale_to_length(BIRD_MAX_SPEED)
        elif self.velocity.length_squared() < (BIRD_MIN_SPEED*BIRD_MIN_SPEED):
            self.velocity.scale_to_length(BIRD_MIN_SPEED)
    
    def updatePosition(self):
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

        speed=random.random() * (BIRD_MAX_SPEED-BIRD_MIN_SPEED) + BIRD_MIN_SPEED
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



#####-----------------------------------------------------------------------------------------------------------------------------
#### Graphics
#####-----------------------------------------------------------------------------------------------------------------------------
class Graphics:
    world:World

    def __init__(self,world:World):
        self.world = world

    def draw(self,screen):
        self.drawFlock(screen)

    def drawFlock(self,screen):
        f = self.world.flock
        for aBird in f.birds:
            self.drawBird(aBird,screen)

    def drawBird(self,bird:Bird,screen):
        heading = Vector2(bird.velocity)
        heading.scale_to_length(BIRD_LENGTH)
        if(self.world.drawDiagnostics):
            if(bird.gravity != None):
                pygame.draw.circle(screen,Color(230,230,255,a=.10),center=bird.pos,radius=BIRD_VISIBILITY)
                pygame.draw.line(screen,(0,0,255),bird.pos,bird.gravity,1)
            else:
                pygame.draw.circle(screen,Color(255,230,230,a=.10),center=bird.pos,radius=BIRD_VISIBILITY)
        pygame.draw.line(screen,(255,0,0),bird.pos,bird.pos+heading,2)



#####-----------------------------------------------------------------------------------------------------------------------------
#### USer Input/Events
#####-----------------------------------------------------------------------------------------------------------------------------
def processEvents(world):
    # this is called "event driven programming."  When stuff
    # happens in the computer's environment, it puts an event in a list.
    # your code looks at the list from time to time to see what's happened, and 
    # reacts accordingly
    for event in pygame.event.get():
        if event.type == QUIT:
            return True
        if event.type == KEYDOWN:
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
def draw(world,graphics,surface,screen):
    # this is where you draw the screen based on what the current state of your world is.
    surface.fill((250,250,250))    
    graphics.draw(surface)
    screen.blit(surface,(0,0))
    pygame.display.flip()


#---------------------------------------------------------------------------
#
# The main program
#
#---------------------------------------------------------------------------

def runLoop(world,graphics,surface,screen):
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
        draw(world,graphics,surface,screen)


#####-----------------------------------------------------------------------------------------------------------------------------
#### Main program
#####-----------------------------------------------------------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
    surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
    pygame.display.set_caption('Boids')

    # initialize the world
    world:World = World(WORLD_WIDTH,WORLD_HEIGHT)

    # initialize graphics
    graphics = Graphics(world)

    world.reset()

    draw(world,graphics,surface,screen)

    # Event loop
    runLoop(world,graphics,screen,surface)



if __name__ == '__main__': main()
