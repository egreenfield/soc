from typing import Hashable

from pygame.math import Vector2


class ListPartition:
    itemList:list[any]

    def __init__(self) -> None:
        self.itemList = []

    def register(self,o:Hashable):
        self.itemList.append(o)

    def set(self,o:Hashable,pos:Vector2):
        pass

    def clear(self):
        self.itemList = []

    def remove(self,o):
        pass

    def findInCircle(self,center:Vector2,radius:float,skip=None):
        nearby = []
        max2 = radius*radius
        for anItem in self.itemList:
            if anItem == skip:
                continue
            itemPos = anItem.pos
            delta = itemPos - center
            d2 = delta.length_squared()
            if(d2 < max2):
                nearby.append(anItem)
        return nearby

    def findInCone(self,pos:Vector2,dir:Vector2,fovDeg:float,radius:float,skip=None):
        nearby = []
        max2 = radius*radius
        for anItem in self.itemList:
            if(anItem == skip):
                continue
            delta = anItem.pos - pos
            d2 = delta.length_squared()
            if(d2 >= max2):
                continue
            a = dir.angle_to(delta)
            if abs(a) > fovDeg/2:
                continue
            nearby.append(anItem)
        return nearby
