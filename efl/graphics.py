from flock import Repulsor
import pygame
from constants import *
from pygame.locals import *
from parameters import params
from world import World
from bird import Bird
from pygame.math import Vector2
import math


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
        for aRep in f.repulsors:
            self.drawRepulsor(aRep)

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
    
    def drawWedge(self,color,center,radius,angle,angleWidth):
        rc=pygame.Rect(center[0]-radius,center[1]-radius,radius*2,radius*2)
        pygame.draw.arc(self.debugSurface,color,rc,angle-angleWidth/2,angle+angleWidth/2,2)
        rad1 = Vector2(radius,0).rotate_rad(-angle+angleWidth/2)
        pygame.draw.line(self.debugSurface,color,center,center+rad1,2)
        rad1 = Vector2(radius,0).rotate_rad(-angle-angleWidth/2)
        pygame.draw.line(self.debugSurface,color,center,center+rad1,2)

    def drawDiagnostics(self,bird:Bird):
        angle = bird.velocity.as_polar()[1]/180 * math.pi
        if(bird.gravity != None):
            self.drawWedge(Color(230,230,255,200),bird.pos,params.birdVisibility,-angle,params.fov*math.pi/180)
#            pygame.draw.circle(self.debugSurface,Color(230,230,255,150),center=bird.pos,radius=params.birdVisibility)
            if(not bird.didWrap):
                pygame.draw.line(self.birdSurface,(0,0,255),bird.pos,bird.gravity,1)
        else:
            self.drawWedge(Color(255,230,230,200),bird.pos,params.birdVisibility,-angle,params.fov*math.pi/180)

    def drawBird(self,bird:Bird):
        heading = Vector2(bird.velocity)
        heading.scale_to_length(BIRD_LENGTH)
        if(self.world.drawDiagnostics):
            self.drawDiagnostics(bird)
        pygame.draw.line(self.birdSurface,(255,0,0),bird.pos,bird.pos+heading,2)
        if(self.world.drawTails):
            self.drawTails(bird)
    def drawRepulsor(self,rep:Repulsor):
        pygame.draw.circle(self.birdSurface,Color(0,0,0,150),center=rep.pos,radius=REPULSOR_DRAW_RADIUS)
