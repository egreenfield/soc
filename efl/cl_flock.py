import numpy as np
import pyopencl as cl
import os
from parameters import params
from constants import *
import math

class CLFlock:

    clInitilized:bool = False
    clBuffersInitiazed:bool = False
    birdCount:int = 0
    updateBirds:cl.Kernel = None
    inputData:np.array
    outputData:np.array
    inputBuffer:cl.Buffer
    outputBuffer:cl.Buffer
    
    objectBuffer:cl.Buffer
    objectCount:int = 0
    world = None

    def __init__(self,world):
        self.world = world
        self.initCL()

    def runUpdate(self,timeDelta:float):
        #print(f"********************************************************")
        #print(f"input:{self.inputData}")
        cl.enqueue_copy(self.queue,self.inputBuffer, self.inputData)
        if(self.objectCount > 0):
            cl.enqueue_copy(self.queue,self.objectBuffer, self.objectData)
            #print(f"input:{self.objectData}")
        self.updateBirds(self.queue, (self.birdCount,1), None, 
            self.inputBuffer, self.outputBuffer,
            self.objectBuffer,
            timeDelta/1000.0,
            self.birdCount, self.objectCount,
            self.world.width,self.world.height,
            params.birdVisibility,params.fov * math.pi/180.,
            params.gravitationalStrength,
            params.tooClose,
            params.individuality,
            0 if (self.world.edgeBehavior == EDGE_WRAP) else params.boxMagnetism,
            params.repulsionStrength
        )
        cl.enqueue_copy(self.queue, self.outputData, self.outputBuffer)
        #print(f"ouput:{self.outputData}")

    def initCL(self):
        os.environ["PYOPENCL_CTX"]=":1"
        self.initilized = True
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)
        with open('./birdUpdate.cl', 'r') as f:
            kernelsource = f.read()
        prg = cl.Program(self.ctx, kernelsource).build()
        self.updateBirds = prg.updateBirds  # Use this Kernel object for repeated calls
        # input data, output data, width, height
        self.updateBirds.set_scalar_arg_dtypes([
            None, None, None,
            np.float32, 
            np.uint32, np.uint32,
            np.uint32, np.uint32,
            np.float32, np.float32,
            np.float32, np.float32,
            np.float32,
            np.float32,
            np.float32
        ])

        self.clInitilized = True

    def setBuffers(self,inputData,outputData,objectData):
        self.inputData = inputData
        self.outputData = outputData
        self.objectData = objectData


    def setBufferSize(self,birdCount,birdDataSize,objectCount,objectDataSize):
        self.clearBuffers()
        mf = cl.mem_flags
        self.birdCount = birdCount
        self.inputBuffer = cl.Buffer(self.ctx, mf.READ_ONLY, birdDataSize)
        self.outputBuffer = cl.Buffer(self.ctx, mf.WRITE_ONLY, birdDataSize)

        self.objectCount = objectCount
        self.objectBuffer = cl.Buffer(self.ctx,mf.READ_ONLY,max(1,objectDataSize))
        
        self.clBuffersInitiazed = True

    def clearBuffers(self):
        self.inputBuffer = None
        self.outputBuffer = None
        self.clBuffersInitiazed = False    