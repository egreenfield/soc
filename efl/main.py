from dataclasses import dataclass
from typing import Tuple
import pygame
from pygame.locals import *
from pygame.math import Vector2
import random
import math
from pygame import Surface

WORLD_WIDTH     = 1800
WORLD_HEIGHT    = 900
BIRD_HEIGHT = 10
BIRD_WIDTH = 3
BIRD_MAX_SPEED = 350
BIRD_MIN_SPEED = 160
NUM_BIRDS = 200
BIRD_LENGTH = 10
BIRD_VISIBILITY = 100
BOX_MAGNETISM = 2000
TOO_CLOSE = 10
INDIVIDUALITY = 8

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

class Bird:
    pos:Vector2
    heading:float
    newPos:Vector2
    flock:any
    def __init__(self,flock,pos,heading,speed):
        self.pos = pos
        self.heading = heading
        self.velocity = Vector2(speed,0).rotate(heading)
        self.speed = speed
        self.flock = flock

    def calculateNewPosition(self,timeDelta):
        timeDelta = timeDelta / 1000.0
        velocity = Vector2(0,0)

        velocity += + self.currentFlight()
#        velocity += self.stayInBox(self.flock.world.width,self.flock.world.height)

        nearbyBirds = self.flock.findBirdsNearby(self.pos,BIRD_VISIBILITY)        
        if(len(nearbyBirds) > 0):
            velocity += self.flyTowardsToNearbyBirds(nearbyBirds)
            velocity += self.stayAway(nearbyBirds)
            velocity += self.stayAway(nearbyBirds)

        self.velocity = velocity
        self.limitSpeed()

        delta = velocity * timeDelta        
        self.newPos = self.pos + delta
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
        return delta * .01
    
    def fitIn(self,nearbyBirds):
        delta = Vector2(0,0)
        for aBird in nearbyBirds:
            delta += aBird.velocity
        delta /= len(nearbyBirds)
        return (delta - self.velocity) / INDIVIDUALITY
    
    def limitSpeed(self):
        if self.velocity.length_squared() > (self.speed*self.speed):
            self.velocity.scale_to_length(self.speed)


    def updatePosition(self):
        self.pos = self.newPos
        self.newPos = None

class Flock:
    birds:list[Bird]
    world:any = None
    def __init__(self,world):
        self.birds = []
        self.world = world
        pass
    def createRandomBird(self):
        newBird = Bird(self,
        pos=Vector2(self.world.width*random.random(),self.world.height*random.random()),
        heading=random.random()*360,
        speed=random.random() * (BIRD_MAX_SPEED-BIRD_MIN_SPEED) + BIRD_MIN_SPEED
        )
        self.birds.append(newBird)
    def update(self,delta):
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



#---------------------------------------------------------------------------
#
# Defining your data
#
#---------------------------------------------------------------------------

# this is where we define all the 'state' in your world.  'State' is all the data
# a computer needs to be able to function correctly.  In this case, it's all the data
# you need to be able to draw and update the state of the game.
@dataclass
class World:
    playerPosition = None
    flock:Flock
    width:int
    height:int
    def __init__(self,w:int,h:int):
        self.width = w
        self.height = h
        self.flock = Flock(self)


# this is data that gets used to draw the game.  It's separate from the 'state' because 
# it's not really about the mechanics of the game, but only just the data needed to show it on screen
# for example, you might load up some images that you use to represent a player, a bad guy, etc.  
# you don't want to have to load those every time you draw to the screen, so we can load it once, 
# stick it here, and use it every time we draw.
@dataclass
class Graphics:
    text = None
    world:World
    birdSprite:Surface

    def __init__(self,world:World):
        self.world = world
        self.birdSprite = Surface((BIRD_WIDTH,BIRD_HEIGHT),flags=SRCALPHA)
        self.birdSprite.fill((255,0,0))

    def draw(self,screen):
        self.drawFlock(screen)
    def drawFlock(self,screen):
        f = self.world.flock
        for aBird in f.birds:
            self.drawBird(aBird,screen)
    def drawBird(self,bird:Bird,screen):
        # s = pygame.transform.rotate(self.birdSprite,bird.heading)
        # screen.blit(s,(bird.pos[0]-BIRD_WIDTH/2,bird.pos[1]-BIRD_HEIGHT/2))
        heading = Vector2(bird.velocity)
        heading.scale_to_length(BIRD_LENGTH)
        pygame.draw.line(screen,(255,0,0),bird.pos,bird.pos+heading,2)


#---------------------------------------------------------------------------
#
# Handling change
#
#---------------------------------------------------------------------------
def processEvents(world):
    # this is called "event driven programming."  When stuff
    # happens in the computer's environment, it puts an event in a list.
    # your code looks at the list from time to time to see what's happened, and 
    # reacts accordingly
    for event in pygame.event.get():
        if event.type == QUIT:
            return True

    return False

def checkKeys(world):
    # this is called polling.  Instead of getting a list of events,
    # you can ask (i.e., 'poll') things in the computer to find out 
    # what the state of things is, and react accordingly.
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_LEFT]:
        world.textpos = world.textpos.move(-1,0)
    if pressed_keys[K_RIGHT]:
        world.textpos = world.textpos.move(1,0)


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
def draw(world,graphics,screen):
    # this is where you draw the screen based on what the current state of your world is.
    screen.fill((250,250,250))    
    graphics.draw(screen)
    pygame.display.flip()


#---------------------------------------------------------------------------
#
# The main program
#
#---------------------------------------------------------------------------

def runLoop(world,graphics,screen):
    # this is what's called the 'main loop' of the program.  It's basically 
    # how all programs work...apps, games, etc.  Sometimes you write it yourself (like we do here),
    # and sometimes a library handles it for you.  Regardless, the basics are the same...
    # 1) check to see if anything has happened
    # 2) do periodic updates and maintenance
    # 3) update the screen 
    # 4) repeat until it's time to quit
    clock = pygame.time.Clock()

    while 1:
        delta = clock.tick(30)
        shouldQuit = processEvents(world)
        if(shouldQuit):
            return
        checkKeys(world)        
        updateWorld(world,delta)
        draw(world,graphics,screen)



def main():
    # this is the main function of the app.  
    # 1) load up and initialize everything we need.
    # 2) start the main loop running
    # 3) cleanup and quit

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
    pygame.display.set_caption('Boids')


    # initialize the world
    world:World = World(WORLD_WIDTH,WORLD_HEIGHT)

    # initialize graphics
    graphics = Graphics(world)

    for i in range(NUM_BIRDS):
        world.flock.createRandomBird()

    draw(world,graphics,screen)

    # Event loop
    runLoop(world,graphics,screen)



if __name__ == '__main__': main()
