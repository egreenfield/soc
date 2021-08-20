import pygame
from pygame.locals import *
from parameters import Dynamic
from constants import *
from world import World
from graphics import Graphics    
from toolbox import Toolbox

#####-----------------------------------------------------------------------------------------------------------------------------
#### USer Input/Events
#####-----------------------------------------------------------------------------------------------------------------------------
    
def processEvents(world:World):
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
            elif event.key == K_t:
                world.drawTails = not world.drawTails
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            world.mouse.pos = event.pos
            world.flock.addRepulsor(world.mouse)
        if event.type == MOUSEBUTTONUP and event.button == 3:
            world.mouse.pos = event.pos
            world.flock.removeRepulsor(world.mouse)
        if event.type == MOUSEMOTION:
            world.mouse.pos = event.pos

        Toolbox.handleEvent(event)

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
