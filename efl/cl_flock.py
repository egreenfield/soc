import numpy as np
import pyopencl as cl
import os


class CLFlock:

    clInitilized:bool = False
    clBuffersInitiazed:bool = False
    birdCount:int = 0
    updateBirds:cl.Kernel = None
    inputData:np.array
    outputData:np.array
    inputBuffer:cl.Buffer
    outputBuffer:cl.Buffer
    world = None

    def __init__(self,world):
        self.world = world
        self.initCL()

    def runUpdate(self,timeDelta:float):
        #print(f"********************************************************")
        #print(f"input:{self.inputData}")
        cl.enqueue_copy(self.queue,self.inputBuffer, self.inputData)
        self.updateBirds(self.queue, (self.birdCount,1), None, self.inputBuffer, self.outputBuffer,timeDelta/1000.0,self.world.width,self.world.height)
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
        self.updateBirds.set_scalar_arg_dtypes([None, None, np.float32, np.uint32, np.uint32])
        self.clInitilized = True

    def setBuffers(self,inputData,outputData):
        self.inputData = inputData
        self.outputData = outputData

    def setBufferSize(self,birdCount,sampleData):
        self.clearBuffers()
        mf = cl.mem_flags
        self.birdCount = birdCount
        self.inputBuffer = cl.Buffer(self.ctx, mf.READ_ONLY, sampleData.nbytes)
        self.outputBuffer = cl.Buffer(self.ctx, mf.WRITE_ONLY, sampleData.nbytes)
        self.clBuffersInitiazed = True

    def clearBuffers(self):
        self.inputBuffer = None
        self.outputBuffer = None
        self.clBuffersInitiazed = False    