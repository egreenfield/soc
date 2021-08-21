from typing import Hashable
from dataclasses import dataclass
from pygame.math import Vector2

CELL_SIZE = 100

class SparseList(list):
    negativeOffset = 0

    def __setitem__(self, index, value):
        if isinstance(index,int):
            index += self.negativeOffset
            if(index < 0):
                self[:0] = [None] * (-index)
                self.negativeOffset += (-index)
                index = 0
            missing = index - len(self) + 1
            if missing > 0:
                self.extend([None] * missing)
        list.__setitem__(self, index, value)
    def __getitem__(self, index):
        if isinstance(index,int):
            index += self.negativeOffset
        try: return list.__getitem__(self, index)
        except IndexError: return None


class Cell:
    members:dict
    def __init__(self):
        self.members = {}

class GridPartition:
    itemGrid:SparseList
    itemToCellMap:dict[Cell]

    def __init__(self) -> None:
        self.clear()

    def clear(self):
        self.itemGrid = SparseList()
        self.itemToCellMap = {}

    def posToCellIndex(self,pos):
        return (int(pos.x/CELL_SIZE),int(pos.y/CELL_SIZE))
    
    def getCell(self,index):
        col = None
        cell = None

        col = self.itemGrid[index[0]]
        if col == None:
            self.itemGrid[index[0]] = col = SparseList()

        cell = col[index[1]]
        if cell == None:
            col[index[1]] = cell = Cell()
        return cell

    def posToCell(self,pos):
        return self.getCell(self.posToCellIndex(pos))


    def place(self,o:Hashable):
        cell = self.posToCell(o.pos)
        cell.members[o] = o
        self.itemToCellMap[o] = cell
        
    def register(self,o:Hashable):
        self.place(o)

    def set(self,o:Hashable,pos:Vector2):
        oldCell = self.itemToCellMap[o]
        newCell = self.posToCell(pos)
        if newCell == oldCell:
            return
        del oldCell.members[o]
        newCell.members[o] = o
        self.itemToCellMap[o] = newCell


    def remove(self,o):
        oldCell = self.itemToCellMap[o]
        del oldCell.members[o]
        del self.itemToCellMap[o]

    def buildConsiderList(self,center:Vector2,radius:float) -> list[any]:
        consider = []
        topLeft = self.posToCellIndex(center - Vector2(radius,radius))
        bottomRight = self.posToCellIndex(center + Vector2(radius,radius))
        for x in range(topLeft[0],bottomRight[0]+1):
            for y in range(topLeft[1],bottomRight[1]+1):
                try:
                    cell = self.itemGrid[x][y]
                    consider.extend(cell.members.values())
                except:
                    pass
        return consider

    def findInCircle(self,center:Vector2,radius:float,skip=None):
        consider = self.buildConsiderList(center,radius)
        nearby = []
        max2 = radius*radius
        for anItem in consider:
            if anItem == skip:
                continue
            itemPos = anItem.pos
            delta = itemPos - center
            d2 = delta.length_squared()
            if(d2 < max2):
                nearby.append(anItem)
        return nearby

    def findInCone(self,pos:Vector2,dir:Vector2,fovDeg:float,radius:float,skip=None):
        consider = self.buildConsiderList(pos,radius)
        nearby = []
        max2 = radius*radius
        for anItem in consider:
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
