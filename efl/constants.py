from pygame.locals import *
from parameters import Dynamic

#####-----------------------------------------------------------------------------------------------------------------------------
#### Playback state
#####-----------------------------------------------------------------------------------------------------------------------------

CONTINUOUS = 0
STOP = 1
STEP = 2
STARTING_RUNSTYLE = CONTINUOUS

EDGE_WRAP = 0
EDGE_RETURN = 1
EDGE_DEFAULT_BEHAVIOR = EDGE_RETURN

EDGE_MARGIN = 200
#####-----------------------------------------------------------------------------------------------------------------------------
#### Graphics Constants
#####-----------------------------------------------------------------------------------------------------------------------------

WORLD_WIDTH     = 1800
WORLD_HEIGHT    = 900
STARTING_BIRD_COUNT = 100
BIRD_LENGTH = 10
TAIL_LENGTH = 20


#####-----------------------------------------------------------------------------------------------------------------------------
#### Dynamic Parameters
#####-----------------------------------------------------------------------------------------------------------------------------


class Parameters:
    birdMaxSpeed:float 
    birdMinSpeed:float 
    birdVisibility:float
    boxMagnetism:float 
    tooClose:float 
    individuality:float
    gravitationalStrength:float
    fov:float

params = Parameters()

Dynamic.track(params)
Dynamic.add(name='birdMaxSpeed',code=K_m,key="m",min=20,max=1000,value=350)
Dynamic.add(name='birdMinSpeed',code=K_n,key="n",min=20,max=1000,value=270)
Dynamic.add(name='birdVisibility',code=K_v,key="v",min=1,max=200,value=80)
Dynamic.add(name='boxMagnetism',code=K_x,key="x",min=1,max=200,value=10)
Dynamic.add(name='tooClose',code=K_c,key="c",min=1,max=100,value=20)
Dynamic.add(name='individuality',code=K_i,key="i",min=1,max=100,value=5)
Dynamic.add(name='gravitationalStrength',code=K_g,key="g",min=0,max=1,value=.05)
Dynamic.add(name='fov',code=K_f,key="f",min=0,max=360,value=120)
