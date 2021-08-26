
#define kPx 0
#define kPy 1
#define kVx 2
#define kVy 3
#define kBirdSize 4

    __kernel void updateBirds(
        __global const float *birdData, __global float *outputData, const float elapsedSeconds,const int worldWidth,const int worldHeight)
    {
        
        int birdIndex = get_global_id(0);
        const unsigned int birdBase = birdIndex * kBirdSize;

        float pX = birdData[birdBase + kPx];
        float pY = birdData[birdBase + kPy];
        float vX = birdData[birdBase + kVx];
        float vY = birdData[birdBase + kVy];

        pY = pY + vY * elapsedSeconds;
        pX = pX + vX * elapsedSeconds;

        if (pX < 0)
            pX = pX + worldWidth;
        if (pX > worldWidth)
            pX = (pX - worldWidth);
        if (pY < 0)
            pY = pY + worldHeight;
        if (pY > worldHeight)
            pY = (pY - worldHeight);

        outputData[birdBase + kPx] = pX;
        outputData[birdBase + kPy] = pY;
        outputData[birdBase + kVx] = vX;
        outputData[birdBase + kVy] = vY;


    }
