from dataclasses import dataclass
import pygame
from pygame.locals import *


#---------------------------------------------------------------------------
#
# Defining your data
#
#---------------------------------------------------------------------------

SPEED = 0.5
LENGTH = 1000
HEIGHT = 500
PAD_HEIGHT = 50
PAD_WIDTH = 10

# this is where we define all the 'state' in your world.  'State' is all the data
# a computer needs to be able to function correctly.  In this case, it's all the data
# you need to be able to draw and update the state of the game.
@dataclass
class World:
    # textpos = None
    ballpos = None
    pad1pos = 0
    pad2pos = None
    ballvelo = None
    score = [0,0]
    paddle1= None
    paddle2 = None
# this is data that gets used to draw the game.  It's separate from the 'state' because 
# it's not really about the mechanics of the game, but only just the data needed to show it on screen
# for example, you might load up some images that you use to represent a player, a bad guy, etc.  
# you don't want to have to load those every time you draw to the screen, so we can load it once, 
# stick it here, and use it every time we draw.
@dataclass
class Graphics:
    # text = None
    pass

class Paddle:
    yPosition = 0
    xPosition = None
    color = None
    upKey = None
    downKey = None

    def __init__(self,upKey,downKey):
        self.upKey = upKey
        self.downKey = downKey

    def setColor(self,color):
        self.color=color

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.xPosition,self.yPosition,PAD_WIDTH,PAD_HEIGHT))

    def checkKeys(self):
        pressed_keys = pygame.key.get_pressed()
        if self.yPosition>0:
            if pressed_keys[self.upKey]:
                self.yPosition -= SPEED
        if self.yPosition < (HEIGHT-PAD_HEIGHT):
            if pressed_keys[self.downKey]:
                self.yPosition += SPEED
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
    world.paddle1.checkKeys()
    world.paddle2.checkKeys()


    

def updateWorld(world):
    # this is a good place to make updates to the game world that 
    # doesn't happen in response to an event.  Like, say, if a ball is flying through space
    # then you need to update its position because time has passed.
    pass


#---------------------------------------------------------------------------
#
# Drawing
#
#---------------------------------------------------------------------------
def draw(world,graphics,screen):
    # this is where you draw the screen based on what the current state of your world is.
    screen.fill((250,250,250))    
    world.paddle1.draw(screen)
    world.paddle2.draw(screen)
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
    while 1:
        shouldQuit = processEvents(world)
        if(shouldQuit):
            return
        checkKeys(world)
                
        updateWorld(world)
        draw(world,graphics,screen)



def main():
    # this is the main function of the app.  
    # 1) load up and initialize everything we need.
    # 2) start the main loop running
    # 3) cleanup and quit

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((LENGTH, HEIGHT))
    pygame.display.set_caption('Basic Pygame program')


    # initialize graphics
    graphics = Graphics()
    # font = pygame.font.Font(None, 36)
    # text = font.render("Hello There", 1, (10, 10, 10))
    # graphics.text = text

    # initialize the world
    world = World()
    # world.textpos = graphics.text.get_rect()
    # world.textpos.centerx = screen.get_rect().centerx

    #ceate a paddle
    world.paddle1= Paddle(K_w,K_s)
    world.paddle2= Paddle(K_UP,K_DOWN)
    world.paddle1.xPosition=0
    world.paddle2.xPosition=(LENGTH-PAD_WIDTH)

    world.paddle1.setColor((200,0,0))
    world.paddle2.setColor((0,0,200))
    draw(world,graphics,screen)

    # Event loop
    runLoop(world,graphics,screen)



main()
