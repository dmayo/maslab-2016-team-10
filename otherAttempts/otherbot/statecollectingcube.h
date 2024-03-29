#ifndef STATECOLLECTINGCUBE_H
#define STATECOLLECTINGCUBE_H
#include "states.h"

class stateCollectingCube: public states
{
public:
    stateCollectingCube(states * previousState, int color=-1);
    void processData();
    ~stateCollectingCube();
    int myColor;
    int cubeFound;
    int finished;
    long long int myWaitTime;
    double cubeDistance;
};
#endif//STATECOLLECTINGCUBE_H
