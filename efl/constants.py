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

BIRD_CHANGE_COUNT = 100

WORLD_WIDTH     = 2300
WORLD_HEIGHT    = 1200
STARTING_BIRD_COUNT = 100
BIRD_LENGTH = 6
TAIL_LENGTH = 13
REPULSOR_DRAW_RADIUS = 5
DEFAULT_REPULSOR_RADIUS = 150
MOUSE_HIT_DISTANCE = 20
DEFAULT_BOX_MAGNETISM = .05
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
