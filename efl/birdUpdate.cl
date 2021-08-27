
#define kPx 0
#define kPy 1
#define kVx 2
#define kVy 3
#define kBirdSize 4
#define BirdType float8

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

    __kernel void updateBirds(
        __global const BirdType *birds, __global BirdType *outputData, 
        const float elapsedSeconds,
        const int birdCount, const int worldWidth,const int worldHeight,
        const float visibility,const float fov,
        const float gravitationalStrength, const float tooClose,
        const float individuality
    )
    {
        
        // load values
        int birdIndex = get_global_id(0);
        const BirdType bird = birds[birdIndex];


        float2 gravity = (0,0);
        float2 forces = (0,0);
        float2 headingChange = (0,0);
        float2 socialDistance = (0,0);
        
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

        if (nearbyCount) {
            gravity /= nearbyCount;
            forces += (gravity - bird.xy) / gravitationalStrength;
            headingChange /= nearbyCount;
            forces += (headingChange - bird.zw) / individuality;

        }
        forces += socialDistance;


        // apply forces
//        bird.zw += forces;

        bird.zw = limitSpeed(bird.zw);
        
        // apply velocity
        bird.xy += bird.zw * elapsedSeconds;

        // wrap
        if (bird.x < 0)
            bird.x = bird.x + worldWidth;
        if (bird.x > worldWidth)
            bird.x = (bird.x - worldWidth);
        if (bird.y < 0)
            bird.y = bird.y + worldHeight;
        if (bird.y > worldHeight)
            bird.y = (bird.y - worldHeight);

        // store diagnostics
        bird[4] = nearbyCount;
        // bird.s45 = (1,0);//nearbyCount;
        //return
        outputData[birdIndex] = bird;
    }
