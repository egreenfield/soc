
#define kPx 0
#define kPy 1
#define kVx 2
#define kVy 3
#define kBirdSize 4
#define BirdType float8

float2 wrap(float2 pos,const int worldWidth,const int worldHeight,int* didWrap);
float2 limitSpeed(const float2 v);
float2 stayInBox(float2 pos,
                    const int worldWidth,const int worldHeight,
                    const float boxMagnetism);


float2 limitSpeed(const float2 v) {
    // max = params.birdMaxSpeed
    // min = params.birdMinSpeed
    // if velocity.length_squared() > (max*max):
    //     velocity.scale_to_length(max)
    // elif velocity.length_squared() < (min*min):
    //     velocity.scale_to_length(min)
    // return velocity
    float maxSpeed = 350;
    float minSpeed = 270;
    float l2 = (v.x*v.x)+(v.y*v.y);
    float adjustmentRatio = 1;
    if (l2 > maxSpeed*maxSpeed)
        adjustmentRatio = (maxSpeed)/sqrt(l2);
    else if (l2 < minSpeed*minSpeed)
        adjustmentRatio = (minSpeed)/sqrt(l2);
    return v * adjustmentRatio;
}

float2 stayInBox(float2 pos,
                    const int worldWidth,const int worldHeight,
                    const float b) {
    float2 delta = (0,0);
    const float margin = 200;        
    if(pos.x < margin)
        delta.x  += (margin - pos.x)*b;
    else if (pos.x > worldWidth - margin)
        delta.x -= (pos.x-(worldWidth-margin))*b;
    if(pos.y < margin)
        delta.y  += (margin - pos.y)*b;
    else if (pos.y > worldHeight - margin)
        delta.xy-= (pos.y-(worldHeight-margin))*b;
    return delta;
}

float2 wrap(float2 pos,const int worldWidth,const int worldHeight,int* didWrap) {
    // wrap
    if (pos.x < 0) {
        *didWrap = 1;
        pos.x = pos.x + worldWidth;
    } if (pos.x > worldWidth) {
        *didWrap = 1;
        pos.x = (pos.x - worldWidth);
    } if (pos.y < 0) {
        *didWrap = 1;
        pos.y = pos.y + worldHeight;
    } if (pos.y > worldHeight) {
        *didWrap = 1;
        pos.y = (pos.y - worldHeight);
    }
    return pos;
}

__kernel void updateBirds(
    __global const BirdType *birds, __global BirdType *outputData, 
    const float elapsedSeconds,
    const int birdCount, const int worldWidth,const int worldHeight,
    const float visibility,const float fov,
    const float gravitationalStrength, const float tooClose,
    const float individuality,
    const float boxMagnetism
)
{
    
    // load values
    int birdIndex = get_global_id(0);
    const BirdType bird = birds[birdIndex];


    float2 gravity = (0,0);
    float2 forces = (0,0);
    float2 headingChange = (0,0);
    float2 socialDistance = (0,0);
    int didWrap = 0;

    float max2 = visibility*visibility;
    float tc2 = tooClose*tooClose;
    int nearbyCount = 0;
    for (int i=0;i<birdCount;i++) {
            if (i == birdIndex)
            continue;
        BirdType friend = birds[i];
        float d2 = (friend.x - bird.x)*(friend.x - bird.x) +
                        (friend.y - bird.y)*(friend.y - bird.y);
        
        // visible
        if (d2 < max2) {
            nearbyCount++;
            // add gravity
            gravity += friend.xy;
            // add heading
            headingChange += friend.zw;

            // social distancing
            if (d2 < tc2) {
                socialDistance -= (friend.xy - bird.xy);
            }            
        
        }
    }

    if (boxMagnetism > 0) {
        forces += stayInBox(bird.xy,worldWidth,worldHeight,boxMagnetism);
    }

    if (nearbyCount) {
        gravity /= nearbyCount;
        forces += (gravity - bird.xy) * gravitationalStrength;
        headingChange /= nearbyCount;
        forces += (headingChange - bird.zw) / individuality;

    }
    forces += socialDistance;


    // apply forces
    bird.zw += forces;

    bird.zw = limitSpeed(bird.zw);
    
    // apply velocity
    bird.xy += bird.zw * elapsedSeconds;

    if (boxMagnetism <= 0) {
        bird.xy = wrap(bird.xy,worldWidth,worldHeight,&didWrap);
    }

    // store diagnostics
    if (didWrap) {
        bird[4] = 0;
        bird[5] = 0;
    }
    else {
        bird[4] = gravity.x;
        bird[5] = gravity.y;
    }
    outputData[birdIndex] = bird;
}
