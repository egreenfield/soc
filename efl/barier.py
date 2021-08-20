

from flock import Repulsor
from pygame.constants import *
from world import World
import pygame


class BarrierTool:
    key:str = 'b'
    code:int = K_b
    name:str = "barrier"
    world:World = None
    def __init__(self,world):
        self.world = world
        pass

    def addBarrier(self,event):
        r = Repulsor(event.pos)
        self.world.flock.addRepulsor(r)
        print(f"added barrier at {event.pos}")

    def start(self,event):
        keys=pygame.key.get_pressed()
        if keys[K_LSHIFT]:
            self.addBarrier(event)

    def move(self,event):
        pass

    def end(self,event):
        pass
    def getHelp(self):
            return f"{self.key}:{self.name}\n"
