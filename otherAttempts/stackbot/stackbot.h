#ifndef STACKBOT_H
#define STACKBOT_H
//#include "states.h"
//#include "statestart.h"
//#include "sensorsmodule.h"
//#include "actuators/motorscontrol.h"
//#include "actuators/servoscontrol.h"
//#include "actuators/actuator.h"
#include "imageProcessing/ImageProcessor.h"
//#include "mapping/map.h"
//#include "localization/particlefilter.h"
//#include "logger.h"
#include "utils.h"

class stackbot
{
public:
    stackbot();
    void run();
    void run(int argc, char** argv);
    int running;
private:
    //sensorsModule mySensors;
    //motorsControl myMotorControl;
    //servosControl myServosControl;
    //actuator myActuator;
    utils myUtils;
    //states * myState;
    //states * previousState; //necessary for thread safety
    ImageProcessor myImageProcessor;
    //logger myLogger;
};

#endif // STACKBOT_H
