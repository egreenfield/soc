from diagnostics import Diagnostics
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
    font:pygame.font = None

    def __init__(self,world:World):
        self.world = world
        self.screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
        self.birdSurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
        self.tailSurface = self.birdSurface # pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
        self.debugSurface = self.birdSurface #pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
        self.repulsorSurface = self.birdSurface # pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT),flags=SRCALPHA,depth=32)
        self.font = pygame.font.SysFont(None, 24)

    def draw(self):
        self.screen.fill((250,250,250))    
        self.birdSurface.fill((0,0,0,0))    
        if(self.world.drawTails):
            self.tailSurface.fill((0,0,0,0))    
        if(len(self.world.flock.repulsors)):
            self.repulsorSurface.fill((0,0,0,0))    
        if(self.world.drawDiagnostics):
            self.debugSurface.fill((0,0,0,0))    
        self.drawFlock()
        if(self.world.drawDiagnostics):
            self.screen.blit(self.debugSurface,(0,0))
        if(len(self.world.flock.repulsors)):
            self.screen.blit(self.repulsorSurface,(0,0))
        if (self.world.drawTails):
            self.screen.blit(self.tailSurface,(0,0))
        self.screen.blit(self.birdSurface,(0,0))
        self.drawDiagnostics()

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
    
    def drawWedge(self,color,center,radius,angle,angleWidth,weight):
        rc=pygame.Rect(center[0]-radius,center[1]-radius,radius*2,radius*2)
        pygame.draw.arc(self.debugSurface,color,rc,angle-angleWidth/2,angle+angleWidth/2,weight)
        rad1 = Vector2(radius,0).rotate_rad(-angle+angleWidth/2)
        pygame.draw.line(self.debugSurface,color,center,center+rad1,weight)
        rad1 = Vector2(radius,0).rotate_rad(-angle-angleWidth/2)
        pygame.draw.line(self.debugSurface,color,center,center+rad1,weight)

    def drawDiagnosticOverlay(self,bird:Bird):
        angle = bird.velocity.as_polar()[1]/180 * math.pi
        #print(bird.gravity)
        if(bird.gravity.length_squared() > 0):
            self.drawWedge(Color(130,130,255,100),bird.pos,params.birdVisibility,-angle,params.fov*math.pi/180,2)
#            pygame.draw.circle(self.debugSurface,Color(230,230,255,150),center=bird.pos,radius=params.birdVisibility)
            pygame.draw.line(self.birdSurface,(0,0,255,200),bird.pos,bird.gravity,2)
        else:
            self.drawWedge(Color(255,130,130,100),bird.pos,params.birdVisibility,-angle,params.fov*math.pi/180,2)

    def drawBird(self,bird:Bird):
        heading = Vector2(bird.velocity)
        p = bird.pos
        heading.scale_to_length(BIRD_LENGTH)
        if(self.world.drawDiagnostics):
            self.drawDiagnosticOverlay(bird)
        pygame.draw.line(self.birdSurface,(255,0,0),p,p+heading,2)
        if(self.world.drawTails):
            self.drawTails(bird)
        # heading = bird.velocity
        # birdData = self.world.flock.birdData[bird.index]
        # heading.scale_to_length(BIRD_LENGTH)
        # if(self.world.drawDiagnostics):
        #     self.drawDiagnosticOverlay(bird)
        # pygame.draw.line(self.birdSurface,(255,0,0),(birdData[0],birdData[1]),(birdData[0] + heading.x,birdData[1]+heading.x),2)
        # if(self.world.drawTails):
        #     self.drawTails(bird)

    def drawRepulsor(self,rep:Repulsor):
        pygame.draw.circle(self.repulsorSurface,Color(0,0,0,3),center=rep.pos,radius=rep.radius)
        pygame.draw.circle(self.repulsorSurface,Color(0,0,0,150),center=rep.pos,radius=REPULSOR_DRAW_RADIUS)

    def drawDiagnostics(self):
        txt = Diagnostics.getText()
        lines = txt.split("\n")
        y = 5
        for aLine in lines:
            img = self.font.render(aLine, True, (0,0,0))
            rect:Rect = img.get_rect()
            self.screen.blit(img, (5,y))
            y += rect.height
