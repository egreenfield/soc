from dataclasses import dataclass
import pygame
from pygame.locals import *
import random
import math

#---------------------------------------------------------------------------
#
# Defining your data
#
#---------------------------------------------------------------------------

SPEED = 1
LENGTH = 750 
HEIGHT = 500
PAD_HEIGHT = 100
PAD_WIDTH = 10
BALL_SPEED = 5
# this is where we define all the 'state' in your world.  'State' is all the data
# a computer needs to be able to function correctly.  In this case, it's all the data
# you need to be able to draw and update the state of the game.
@dataclass
class World:
    # textpos = None
    ballpos = None
    ballvelo = 2.5
    score = [0,0]
    paddle1= None
    paddle2 = None
    ball=None
    scoreBoard= None
    quit=False
    clock = pygame.time.Clock()

# this is data that gets used to draw the game.  It's separate from the 'state' because 
# it's not really about the mechanics of the game, but only just the data needed to show it on screen
# for example, you might load up some images that you use to represent a player, a bad guy, etc.  
# you don't want to have to load those every time you draw to the screen, so we can load it once, 
# stick it here, and use it every time we draw.
@dataclass
class Graphics:
    pass
class Ball:
    yPosition= None
    xPosition= None
    color = (0,0,0)
    angle=None
    radius=10
    changeX=None
    changeY=None
    def setPos(self):
        self.xPosition=random.randint(int(LENGTH/3),int(LENGTH*2/3))
        self.yPosition=random.randint(50,HEIGHT-50)
    def setAngle(self):
        self.angle=random.randint(30,60)
    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.xPosition,self.yPosition),self.radius)
    def calcChange(self):
        radians= self.angle*math.pi/180
        negativeXChange= bool(random.getrandbits(1))
        negativeYChange= bool(random.getrandbits(1))
        self.changeX= BALL_SPEED*(math.cos(radians))
        self.changeY = BALL_SPEED*(math.sin(radians))
        if negativeXChange:
            self.changeX= -self.changeX
        if negativeYChange:
            self.changeY= -self.changeY
    def move(self):
        self.xPosition+=self.changeX
        self.yPosition-=self.changeY
    def wallCheck(self):
        if self.yPosition<=(0+self.radius) or self.yPosition>=(HEIGHT-self.radius):
            self.changeY= -self.changeY
    def paddleCheck(self,padY,padX):
        #How do I condense this?
        if abs(padX-self.xPosition)<=self.radius:
            if (self.yPosition-self.radius)>padY and (self.yPosition-self.radius)<(padY+PAD_HEIGHT):
                self.changeX = -self.changeX
            elif (self.yPosition+self.radius)>padY and (self.yPosition-self.radius)<(padY+PAD_HEIGHT):
                self.changeX = -self.changeX
            #if (self.yPosition)>padY and (self.yPosition)<(padY+PAD_HEIGHT):
    def checkGoal(self,score,screen,world):
        if self.xPosition<-5:
            score[1]+=1

            world.paddle2.speed-=0.1
            
            self.setPos()
            self.setAngle()
            self.calcChange()
            self.draw(screen)
        elif (self.xPosition-LENGTH)>5:
            score[0]+=1
            
            world.paddle1.speed-=0.1
            self.setPos()
            self.setAngle()
            self.calcChange()
            self.draw(screen)
        
                
class Paddle:
    yPosition = 0
    xPosition = None
    color = None
    upKey = None
    downKey = None
    speed = 5
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
                self.yPosition -= self.speed
        if self.yPosition < (HEIGHT-PAD_HEIGHT):
            if pressed_keys[self.downKey]:
                self.yPosition += self.speed

class scoreBoard:
    def draw(self,red,blu,screen):
        #explain this????
        font = pygame.font.Font('freesansbold.ttf', 32)
        text1 = font.render(str(red),True, (200, 0, 0))
        text2 = font.render(str(blu), True, (0,0,200))
        text1Rect= text1.get_rect(center=(50,50))
        text2Rect= text2.get_rect(center= ((LENGTH-50),50))
        screen.blit(text1,text1Rect)
        screen.blit(text2,text2Rect)


#---------------------------------------------------------------------------
#
# Handling change
#
#---------------------------------------------------------------------------
#HELP
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


    

def updateWorld(world,screen):
    # this is a good place to make updates to the game world that 
    # doesn't happen in response to an event.  Like, say, if a ball is flying through space
    # then you need to update its position because time has passed.
    if world.score[0]==10:
        world.quit=True
                
    if world.score[1]==10:
        world.quit=True
                
    world.ball.wallCheck()
    world.ball.paddleCheck(world.paddle1.yPosition,PAD_WIDTH)
    world.ball.paddleCheck(world.paddle2.yPosition,(LENGTH-PAD_WIDTH))
    world.ball.move()
    world.ball.checkGoal(world.score,screen,world)
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
    world.ball.draw(screen)
    world.scoreBoard.draw(world.score[0],world.score[1],screen)
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
        if world.quit:
            return
        checkKeys(world)
                
        updateWorld(world,screen)
        draw(world,graphics,screen)
        world.clock.tick(60)


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

    world.ball=Ball()
    world.ball.setPos()
    world.ball.setAngle()
    world.ball.calcChange()

    world.scoreBoard = scoreBoard()
    draw(world,graphics,screen)

    # Event loop
    runLoop(world,graphics,screen)



main()
