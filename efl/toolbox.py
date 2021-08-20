
from typing import ClassVar
from dataclasses import dataclass
from pygame.locals import *

@dataclass
class Tool:
    key:str
    code:int
    name:str

    def start(self,event):
        pass

    def move(self,event):
        pass

    def end(self,event):
        pass
    def getHelp(self):
            return f"{self.key}:{self.name}\n"

class Toolbox:
    tools: ClassVar[dict[Tool]] = {}    
    activeTool: ClassVar[Tool] = None

    @classmethod
    def registerTool(self,tool):
        self.tools[tool.code] = tool

    @classmethod
    def getTool(self,code:int):
        if code in self.tools:
            return self.tools[code]
        return None

    @classmethod
    def printHelp(self):
        result = ""
        for aTool in self.tools.values():
            result += aTool.getHelp()
        print(result)

    @classmethod
    def handleEvent(self,event):
        if event.type == KEYDOWN:
            if event.key == K_QUESTION or event.key == K_SLASH:
                self.printHelp()
            newTool = self.getTool(event.key)            
            if(newTool != None):
                self.activeTool = newTool
                print(f"Selected tool {newTool.name}")
        if self.activeTool:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.activeTool.start(event)
            if event.type == MOUSEBUTTONUP and event.button == 1:
                self.activeTool.end(event)            
            if event.type == MOUSEMOTION and event.buttons[0]:
                self.activeTool.move(event)
