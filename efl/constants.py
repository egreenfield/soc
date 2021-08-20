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
