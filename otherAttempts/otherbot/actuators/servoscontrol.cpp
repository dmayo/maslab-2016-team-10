#include "servoscontrol.h"
#include <unistd.h>
#include <iostream>

servosControl::servosControl()
{
    armAngle = ARM_START;
    //hookAngle = HOOK_START;
    sortAngle = SORT_START; //initialize this in the center
    previousSwipe=0;
    swipping =0;
    this->running=1;
    std::cout<<"servo controller initialized"<<std::endl;
    runThread = new std::thread(run,this);
}

void servosControl::run(servosControl *myservo){
    std::cout<<"servo controller running"<<std::endl;
    while(myservo->running){
        //std::cout<<"servo controller running"<<std::endl;
        usleep(UPDATE_RATE_SERVOS_MILISECONDS*1000);
        myservo->computeNewServosAngles();
    }
}
/*
void servosControl::hookBlock(){
    hookAngle = HOOK_START + 110;
}

void servosControl::unHookBlock(){
    hookAngle = HOOK_START;
}
*/
void servosControl::raiseBlock(){
    armAngle = ARM_START + 154;
}

void servosControl::unRaiseBlock(){
    armAngle = ARM_START;
}

void servosControl::sortRight(){
    sortAngle = 135;
}

void servosControl::sortLeft(){
    sortAngle = 45;
}

void servosControl::reset(){
    //hookAngle = HOOK_START;
    armAngle = ARM_START;
    sortAngle = SORT_START;
    swipping=0;
}

void servosControl::sweep(){
    swipping=1;
}

void servosControl::stopSweep(){
    swipping=0;
}

servosControl::~servosControl(){
    running=0;
    runThread->join();
    delete runThread;
}
void servosControl::computeNewServosAngles(){
    if (swipping){
        if (previousSwipe){
            sortLeft();
            previousSwipe=0;
        }
        else{
            sortRight();
            previousSwipe=1;
        }
        usleep(SWIPE_TIME_MS*1000);
    }

    /*if (startCollect){
                                                                 hookBlock();
        }
        if (time > TIME_FOR_HOOK )
    }
    else {

    }*/
}
