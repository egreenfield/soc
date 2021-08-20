from constants import *
import pygame
from pygame.locals import *
from world import World
from bird import Bird
from pygame.math import Vector2


#####-----------------------------------------------------------------------------------------------------------------------------
#### Graphics
#####-----------------------------------------------------------------------------------------------------------------------------
class Graphics:
    world:World

    def __init__(self,world:World):
        self.world = world
        self.screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
        self.birdSurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
        self.tailSurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
        self.debugSurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)

    def draw(self):
        self.screen.fill((250,250,250))    
        self.birdSurface.fill((0,0,0,0))    
        self.tailSurface.fill((0,0,0,0))    
        self.debugSurface.fill((0,0,0,0))    
        self.drawFlock()
        self.screen.blit(self.tailSurface,(0,0))
        self.screen.blit(self.debugSurface,(0,0))
        self.screen.blit(self.birdSurface,(0,0))


    def drawFlock(self):
        f = self.world.flock
        for aBird in f.birds:
            self.drawBird(aBird)
    def drawTails(self,bird:Bird):
        start = 0
        try:
            while True:
                end = bird.tails.index(None,start)
                if(end-start >= 2):
                    pygame.draw.lines(self.tailSurface,(0,0,150,50),False,bird.tails[start:end])
                start = end+1
        except:            
            pass
        if(len(bird.tails)-start > 2):
            pygame.draw.lines(self.tailSurface,(0,0,150,50),False,bird.tails[start:])

    def drawDiagnostics(self,bird:Bird):
        if(bird.gravity != None):
            pygame.draw.circle(self.debugSurface,Color(230,230,255,150),center=bird.pos,radius=params.birdVisibility)
            if(not bird.didWrap):
                pygame.draw.line(self.birdSurface,(0,0,255),bird.pos,bird.gravity,1)
        else:
            pygame.draw.circle(self.debugSurface,Color(255,230,230,150),center=bird.pos,radius=params.birdVisibility)

    def drawBird(self,bird:Bird):
        heading = Vector2(bird.velocity)
        heading.scale_to_length(BIRD_LENGTH)
        if(self.world.drawDiagnostics):
            self.drawDiagnostics(bird)
        pygame.draw.line(self.birdSurface,(255,0,0),bird.pos,bird.pos+heading,2)
        if(self.world.drawTails):
            self.drawTails(bird)

