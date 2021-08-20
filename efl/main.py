import pygame
from pygame.locals import *
from parameters import Dynamic
from constants import *
from world import World
from graphics import Graphics    
from toolbox import Tool, Toolbox
from barier import BarrierTool

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
                if event.mod & KMOD_SHIFT:
                    world.reset()
                else:
                    world.resetBirds()
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

def initTools(world:World):

    Dynamic.track(params)
    Dynamic.add(name='birdMaxSpeed',code=K_m,key="m",min=20,max=1000,value=350)
    Dynamic.add(name='birdMinSpeed',code=K_n,key="n",min=20,max=1000,value=270)
    Dynamic.add(name='birdVisibility',code=K_v,key="v",min=1,max=200,value=80)
    Dynamic.add(name='boxMagnetism',code=K_x,key="x",min=1,max=200,value=10)
    Dynamic.add(name='tooClose',code=K_c,key="c",min=1,max=100,value=20)
    Dynamic.add(name='individuality',code=K_i,key="i",min=1,max=100,value=5)
    Dynamic.add(name='gravitationalStrength',code=K_g,key="g",min=0,max=1,value=.05)
    Dynamic.add(name='fov',code=K_f,key="f",min=0,max=360,value=120)
    Dynamic.add(name='repulsionStrength',code=K_q,key="q",min=1,max=10,value=3)

    Toolbox.registerTool(BarrierTool(world))
def main():
    pygame.init()
    pygame.display.set_caption('Boids')

    # initialize the world
    world:World = World(WORLD_WIDTH,WORLD_HEIGHT)

    initTools(world)
    # initialize graphics
    graphics = Graphics(world)

    world.reset()

    draw(world,graphics)

    # Event loop
    runLoop(world,graphics)



if __name__ == '__main__': main()
