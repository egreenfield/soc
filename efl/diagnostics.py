from typing import ClassVar
import pygame
from pygame.locals import *
from constants import *

class Diagnostics:

    diagnostics:ClassVar[dict[str]] = {}

    @classmethod
    def init(self):
        pass

    @classmethod
    def getText(self):
        result = ""
        for aD in self.diagnostics.values():
            if callable(aD):
                result += aD() + "\n"
            else:
                result += aD + "\n"
        return result

    @classmethod
    def setDiagnostic(self,name,value):
        self.diagnostics[name] = value
