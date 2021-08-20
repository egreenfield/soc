
from typing import ClassVar
from pygame.locals import *


class Dynamic:
    name:str
    key:str
    code:int
    min:float
    max:float
    value:float

    dynamicParameters = {}
    readOnlyParams = None

    @classmethod
    def track(self,readOnlyParams):
        self.readOnlyParams = readOnlyParams

    def setValue(self,newValue:float):        
        self.value = newValue
        setattr(Dynamic.readOnlyParams,self.name,newValue)
    
    def adjustValue(self,delta:float):
        v = self.value + delta
        if v > self.max:
            v = self.max
        if v < self.min:
            v = self.min
        self.value = v
        setattr(Dynamic.readOnlyParams,self.name,self.value)

    def mapValue(self,pct:float):
        return self.min + (self.max-self.min)*pct

    def mapRelativeValue(self,pct:float):
        return (self.max-self.min)*pct

    active = None

    @classmethod
    def get(self,code:int):
        if code in self.dynamicParameters:
            return self.dynamicParameters[code]
        return None

    @classmethod
    def add(self,**kwargs):
        p = Dynamic()
        for aKey in kwargs:
            setattr(p,aKey,kwargs[aKey])
        self.dynamicParameters[kwargs['code']] = p #Parameter(**kwargs)
        setattr(Dynamic.readOnlyParams,kwargs['name'],kwargs['value'])

    @classmethod
    def printHelp(self):
        result = ""
        for aParam in self.dynamicParameters.values():
            result += f"{aParam.key}:{aParam.name} ({aParam.value})\n"
        print(result)

    @classmethod
    def adjustByMouse(self, rel, width):
        if self.active == None:
            return

        pct = rel[0] / width
        delta = self.active.mapRelativeValue(pct)
        self.active.adjustValue(delta)    
        print(f"setting {self.active.name} to {self.active.value}")

    @classmethod
    def handleEvent(self,event,width):
        if event.type == KEYDOWN:
            self.active = self.get(event.key)            
            if event.key == K_QUESTION or event.key == K_SLASH:
                self.printHelp()
        if event.type == KEYUP:
            self.active = None
        if event.type == MOUSEMOTION:
            if(event.buttons[0]):
                self.adjustByMouse(event.rel,width)
