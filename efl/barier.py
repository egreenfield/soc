

from pygame.math import Vector2
from flock import Repulsor
from pygame.constants import *
from world import World
import pygame


class BarrierTool:
    key:str = 'b'
    code:int = K_b
    name:str = "barrier"
    world:World = None
    selected:Repulsor = None
    startPoint:Vector2 = None
    startPos:Vector2 = None
    def __init__(self,world):
        self.world = world
        pass

    def addBarrier(self,event):
        r = Repulsor(event.pos)
        self.world.flock.addRepulsor(r)
        print(f"added barrier at {event.pos}")
        return r

        
    def start(self,event):
        keys=pygame.key.get_pressed()
        if keys[K_LSHIFT]:
            self.selected = self.addBarrier(event)
        else:
            self.selected = self.world.flock.findBarrierAtPoint(Vector2(event.pos))
        self.startPoint = Vector2(event.pos)
        if(self.selected):
            self.startPos = self.selected.pos

    def move(self,event):
        if self.selected == None:
            return
        self.selected.pos = self.startPos + (Vector2(event.pos) - self.startPoint)

    def end(self,event):
        self.selected = None

    def getHelp(self):
            return f"{self.key}:{self.name}\n"
