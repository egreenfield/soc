
from typing import ClassVar
from pygame.locals import *
from constants import *
from toolbox import Toolbox

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



    def getHelp(self):
        return f"{self.key}:{self.name} ({self.value})\n"

    def move(self, event):
        rel = event.rel
        width = WORLD_WIDTH
        pct = rel[0] / width
        delta = self.mapRelativeValue(pct)
        self.adjustValue(delta)    
        print(f"setting {self.name} to {self.value}")

    @classmethod
    def add(self,**kwargs):
        p = Dynamic()
        for aKey in kwargs:
            setattr(p,aKey,kwargs[aKey])
        Toolbox.registerTool(p)
        self.dynamicParameters[kwargs['code']] = p #Parameter(**kwargs)
        setattr(Dynamic.readOnlyParams,kwargs['name'],kwargs['value'])




params = Parameters()

Dynamic.track(params)
Dynamic.add(name='birdMaxSpeed',code=K_m,key="m",min=20,max=1000,value=350)
Dynamic.add(name='birdMinSpeed',code=K_n,key="n",min=20,max=1000,value=270)
Dynamic.add(name='birdVisibility',code=K_v,key="v",min=1,max=200,value=80)
Dynamic.add(name='boxMagnetism',code=K_x,key="x",min=1,max=200,value=10)
Dynamic.add(name='tooClose',code=K_c,key="c",min=1,max=100,value=20)
Dynamic.add(name='individuality',code=K_i,key="i",min=1,max=100,value=5)
Dynamic.add(name='gravitationalStrength',code=K_g,key="g",min=0,max=1,value=.05)
Dynamic.add(name='fov',code=K_f,key="f",min=0,max=360,value=120)
