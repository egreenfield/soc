from dataclasses import dataclass
from typing import Tuple
import pygame
from pygame.locals import *

CELL_SIDE=10
DRAW_SIDE=CELL_SIDE-4
SCREEN_SIDE=500
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
    board=None
    speed=4
    def increaseSpeed(self):
        if self.speed>1:
            self.speed-=1
        else:
            self.speed=0.1
    def decreaseSpeed(self):
        self.speed+=1

# this is data that gets used to draw the game.  It's separate from the 'state' because 
# it's not really about the mechanics of the game, but only just the data needed to show it on screen
# for example, you might load up some images that you use to represent a player, a bad guy, etc.  
# you don't want to have to load those every time you draw to the screen, so we can load it once, 
# stick it here, and use it every time we draw.
@dataclass
class Graphics:
    text = None
class Cell:
    Alive=False
    setAlive=False
    xPos=None
    yPos=None
    def checkNeighbors(self,board):
        neighbors=0
        under=False
        over=False
        inLeft=False
        inRight=False
        self.setAlive=self.Alive
        row=board.rows[self.yPos]
        if self.yPos>0:
            under=True
        if self.yPos<(SCREEN_SIDE/CELL_SIDE-1):
            over=True
        if self.xPos>0:
            inLeft=True
        if self.xPos<(SCREEN_SIDE/CELL_SIDE-1):
            inRight=True
        
        if inLeft:
            left=row[self.xPos-1]
            if (left.Alive):
                neighbors+=1

        if inRight:
            right=row[self.xPos+1]
            if (right.Alive):
                neighbors+=1
        
        if under:
            topRow=board.rows[self.yPos-1]
            top = topRow[self.xPos]


            if (top.Alive):
                neighbors+=1
    
        if under and inLeft:
            topLeft= topRow[self.xPos-1]
            if (topLeft.Alive):
                neighbors+=1

        if under and inRight:
            topRight= topRow[self.xPos+1]
            if (topRight.Alive):
                neighbors+=1

        if over:
            bottomRow=board.rows[self.yPos+1]
            bottom = bottomRow[self.xPos]
            if (bottom.Alive):
                neighbors+=1
        
        if over and inRight:
            bottomRight= bottomRow[self.xPos+1]
            if (bottomRight.Alive):
                neighbors+=1
        
        if over and inLeft:
            bottomLeft= bottomRow[self.xPos-1]
            if (bottomLeft.Alive):
                neighbors+=1
        
        if neighbors==3:
            self.setAlive=True
        if neighbors<2 or neighbors>3:
            self.setAlive=False
        
            
class Board:
    enter=True
    rows=[]
    def toggleEnter(self):
        self.enter=not(self.enter)

    def setManual(self,clickPos):
        if (self.enter):
            xPos=clickPos[0]
            yPos=clickPos[1]
            xPos=int(xPos/CELL_SIDE)
            yPos=int(yPos/CELL_SIDE)
            #self.rows[yPos][xPos].Alive= not(self.rows[yPos][xPos].Alive)
            self.rows[yPos][xPos].setAlive=not (self.rows[yPos][xPos].Alive)



    def setGrid(self):
        for x in range(int(SCREEN_SIDE/CELL_SIDE)):
            row=[]
            for y in range(int(SCREEN_SIDE/CELL_SIDE)):
                cell= Cell()
                cell.xPos=y
                cell.yPos=x
                #if y==25 and x==25:

                    #cell.Alive=True
                row.append(cell)
            self.rows.append(row)
    def checkStates(self):
        for row in self.rows:
            for cell in row:
                cell.checkNeighbors(self)
    def updateStates(self):
        for row in self.rows:
            for cell in row:
                cell.Alive=cell.setAlive
    def draw(self,screen):
        yPos=-CELL_SIDE   
        for row in self.rows:
            yPos+=CELL_SIDE
            xPos=-CELL_SIDE
            for cell in row:
                xPos+=CELL_SIDE
                if (cell.Alive):
                    color=(250,0,0)
                else:
                    color=(0,0,0)
                pygame.draw.rect(screen,color,(xPos,yPos,CELL_SIDE-1,CELL_SIDE-1))



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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            world.board.setManual(pos)
        if event.type == pygame.KEYDOWN:
            key=event.key
            if key==K_RETURN:
                world.board.toggleEnter()

    return False

def checkKeys(world):
    # this is called polling.  Instead of getting a list of events,
    # you can ask (i.e., 'poll') things in the computer to find out 
    # what the state of things is, and react accordingly.
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_UP]:
        world.increaseSpeed()
    if pressed_keys[K_DOWN]:
        world.decreaseSpeed()


def updateWorld(world):
    # this is a good place to make updates to the game world that 
    # doesn't happen in response to an event.  Like, say, if a ball is flying through space
    # then you need to update its position because time has passed.
    if not (world.board.enter):
        world.board.checkStates()
    world.board.updateStates()
    pass


#---------------------------------------------------------------------------
#
# Drawing
#
#---------------------------------------------------------------------------
def draw(world,graphics,screen):
    # this is where you draw the screen based on what the current state of your world is.
    #screen.fill((250,250,250))    
    #screen.blit(graphics.text, world.textpos)
    screen.fill((50,50,50))
    world.board.draw(screen)
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
    clock= pygame.time.Clock()
    while 1:
        clock.tick(world.speed)
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
    screen = pygame.display.set_mode((SCREEN_SIDE,SCREEN_SIDE))
    pygame.display.set_caption('Game of LIFE')


    # initialize graphics
    graphics = Graphics()
    #font = pygame.font.Font(None, 36)
    #text = font.render("Hello There", 1, (10, 10, 10))
    #graphics.text = text

    # initialize the world
    world = World()
    world.board=Board()
    world.board.setGrid()

    draw(world,graphics,screen)

    # Event loop
    runLoop(world,graphics,screen)



if __name__ == '__main__': main()
