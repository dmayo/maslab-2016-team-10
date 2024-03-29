#include "stackbot.h"
#include <cstring>
#include <unistd.h>
#include <cstdio>
//#include "statecollectingcube.h"
//#include "statetestprocedure.h"
//#include "statelookingforpurpleline.h"

//actuator * actPointerMain;
stackbot *stackbotPointer;

//Global function that assures that we stop the motors when stopping the robot.
/*
void stopMotorsMain(int signo)
{
    if (signo == SIGINT) {
        stackbotPointer->running=0;
        double a =0;
        actPointerMain->leftWheelPower = &a;
        actPointerMain->rightWheelPower =&a;
        actPointerMain->setPowerLeftWheel(0);
        actPointerMain->setPowerRightWheel(0);
    }
}
*/

stackbot::stackbot(): //Initializes all the modules
    //mySensors(),
    //myMotorControl(&mySensors),
    //myServosControl(),
    //myActuator(myMotorControl,myServosControl),
    myUtils(),
    myImageProcessor()
    //myState(NULL),
    //myLogger(&mySensors, &myMotorControl, &myServosControl, &myState, &myImageProcessor)

{
    //Starts the state machine
    /*
    myState=new stateStart(&myMotorControl,
                           &myServosControl,
                           &mySensors,
                           &myImageProcessor,
                           &myUtils);
    */
    stackbotPointer =this;
    //actPointerMain = &myActuator;
    //signal(SIGINT, stopMotorsMain);
}

//Runs the state machine
void stackbot::run(){
    std::cout << "it works" << std::endl;
    /*
    int changedToPurpleLine=0;
    int decisionPurpleLine = 0;
    while (!mySensors.onData){
        usleep(UPDATE_RATE_STATE_MACHINE_MICROSECONDS);
    }
    myUtils.reset();
    while (running){
        if(myUtils.gameTimeRemaining()>0){
            myState->processData();
            states * nextState = myState->getNextState();
            if (nextState!=myState){
                logger::log();
                previousState = myState;
                myState=nextState;
                delete previousState;
                previousState=NULL;
            }
            usleep(UPDATE_RATE_STATE_MACHINE_MICROSECONDS);
        }
        else{
            myState->stop();
        }
    }
    */
}



void stackbot::run(int argc, char **argv){
/*
    if(strcmp(argv[1],"collectBlock")==0){
        states * nextState = new stateCollectingCube(myState,0);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;

        while (running){
            myState->processData();
            states * nextState = myState->getNextState();
            if (nextState!=myState){ //Makes sure we are always in the same state
                logger::log();
                previousState = nextState;
                delete previousState;
                previousState=NULL;
            }
            usleep(UPDATE_RATE_STATE_MACHINE_MICROSECONDS);
        }
    }

    if(strcmp(argv[1],"goToBlockAndCollect")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        double cubePosition;
        double cubeAngle;
        int cubeColor;
        int answer;
        while (running){
            if (myState->foundCube()){
                cubePosition=myState->getDistanceNearestCube();
                cubeAngle = myState->getAngleNearestCube();
                cubeColor =myState->getColorNearestCube();
                printf("I found a cube at %lf in, %lf, degrees.\n It's color is %d\n' Go to cube? 1, 0\n", cubePosition,cubeAngle, cubeColor);
                scanf("%d", &answer);
                if (answer){
                    myState->finishedGoingToPoint=0;
                    while ((running) && (!myState->finishedGoingToPoint)){
                        myState->startProcessingProceduresManual();
                        myState->goToPoint(cubePosition,cubeAngle);
                        myState->finishProcessingProceduresManual();
                    }
                    printf("Collect Cube? Green=2, Red=1 No= 0\n");
                    scanf("%d", &answer);
                    if (answer){
                        answer--;
                        myState->finishedCollectingBlock=0;
                        while ((running) && (!myState->finishedCollectingBlock)){
                            myState->startProcessingProceduresManual();
                            myState->collectBlock(answer);
                            myState->finishProcessingProceduresManual();
                        }
                    }
                }
            }
        }
    }

    if(strcmp(argv[1],"wallFollow")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        myServosControl.hookBlock();
        myServosControl.hookBlock();
        while (running){
            myState->startProcessingProceduresManual();
            myState->wallFollow();
            myState->finishProcessingProceduresManual();
        }
    }
    if(strcmp(argv[1],"wallFollowRight")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        myServosControl.hookBlock();
        myServosControl.hookBlock();
        while (running){
            myState->startProcessingProceduresManual();
            myState->wallFollowRight();
            myState->finishProcessingProceduresManual();
        }
    }
    if(strcmp(argv[1],"fastWallFollow")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        myServosControl.hookBlock();
        myServosControl.hookBlock();
        while (running){
            myState->startProcessingProceduresManual();
            myState->wallFollowLeftFast();
            myState->finishProcessingProceduresManual();
        }
    }
    if(strcmp(argv[1],"curveRight")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        while (running){
            myState->startProcessingProceduresManual();
            myState->curveToTheRight();
            myState->finishProcessingProceduresManual();
        }
    }

    if(strcmp(argv[1],"mediumCurveRight")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        while (running){
            myState->startProcessingProceduresManual();
            myState->mediumCurveToTheRight();
            myState->finishProcessingProceduresManual();
        }
    }

    if(strcmp(argv[1],"sharpCurveRight")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        while (running){
            myState->startProcessingProceduresManual();
            myState->sharpCurveToTheRight();
            myState->finishProcessingProceduresManual();
        }
    }
    if(strcmp(argv[1],"followCube")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        double cubePosition;
        double cubeAngle;
        double cubeColor;
        while (running){
            myState->startProcessingProceduresManual();
            if(myState->foundCube()){
                cubePosition=myState->getDistanceNearestCube();
                cubeAngle = myState->getAngleNearestCube();
                cubeColor =myState->getColorNearestCube();
                printf("I found a cube at %lf in, %lf, degrees.\n", cubePosition,cubeAngle);
                myState->followPoint(myState->getDistanceNearestCube(), myState->getAngleNearestCube());
            }
            else
                myState->stop();
            myState->finishProcessingProceduresManual();
            usleep(UPDATE_RATE_STATE_MACHINE_MICROSECONDS);
        }
    }

    if(strcmp(argv[1],"colorDetec")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;


        while (running){
            myState->startProcessingProceduresManual();
            if (myState->isCubeRed()) {
                printf("red\n");
            }
            else {
                printf("no\n");
            }

            myState->finishProcessingProceduresManual();
            usleep(500000);
            usleep(UPDATE_RATE_STATE_MACHINE_MICROSECONDS);
        }
    }

    if(strcmp(argv[1],"cubeColorCollect")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        int cubeColor=0;
        int cubeDetected=0;
        while (running){
            myState->startProcessingProceduresManual();
            if (cubeDetected){
                myState->collectBlock();
                if(myState->finishedCollectingBlock){
                    cubeDetected=0;
                }
            }
            else{
                if(myState->detectedCube()){
                    cubeDetected=1;
                    if (myState->isCubeRed()) {
                        cubeColor=1;
                    }
                    else {
                        cubeColor=0;
                    }
                }
            }
            myState->finishProcessingProceduresManual();
            usleep(UPDATE_RATE_STATE_MACHINE_MICROSECONDS);
        }
    }

    if(strcmp(argv[1],"turn360slowly")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        int cubeColor=0;
        int cubeDetected=0;
        while (running){
            myState->startProcessingProceduresManual();
            if(!myState->finishedTurningNDegreesSlowly){
                myState->turnNDegreesSlowly(360);
            }
            else{
                printf("finished turning 360 slowly\n");
            }

            myState->finishProcessingProceduresManual();
            usleep(UPDATE_RATE_STATE_MACHINE_MICROSECONDS);
        }
    }

    if(strcmp(argv[1],"cubeColor")==0){
        states * nextState = new stateTestProcedure(myState);
        logger::log();
        previousState=myState;
        myState = nextState;
        delete previousState;
        previousState=NULL;
        int cubeColor=0;
        int cubeDetected=0;
        while (running){

            if(myState->detectedCube()){
                cubeDetected=1;
                if (myState->isCubeRed()) {
                    printf("cube is red\n");
                    cubeColor=1;
                }
                else {
                    printf("cube is green\n");

                    cubeColor=0;
                }
            }

            usleep(UPDATE_RATE_STATE_MACHINE_MICROSECONDS);
        }
    }

*/
}
