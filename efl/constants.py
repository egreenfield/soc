from pygame.locals import *

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

TARGET_FRAME_RATE = 30

EDGE_MARGIN = 200
#####-----------------------------------------------------------------------------------------------------------------------------
#### Graphics Constants
#####-----------------------------------------------------------------------------------------------------------------------------


RUNNING_TIME = 0
STARTING_BIRD_COUNT = 200
BIRD_CHANGE_COUNT = 100 

# uncomment for profiling setup
#RUNNING_TIME = 15
#STARTING_BIRD_COUNT = 1400

WORLD_WIDTH     = 2300
WORLD_HEIGHT    = 1200
BIRD_LENGTH = 6
TAIL_LENGTH = 13
REPULSOR_DRAW_RADIUS = 5
DEFAULT_REPULSOR_RADIUS = 150
MOUSE_HIT_DISTANCE = 20
DEFAULT_BOX_MAGNETISM = .23
DEFAULT_INDIVIDUALITY = 13
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
    repulsionStrength:float
    fov:float

params = Parameters()
