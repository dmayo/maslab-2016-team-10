#include "statelookingforblocks.h"
#include "stateapproachblock.h"
#include "statecollectingcube.h"
#include <iostream>

stateLookingForBlocks::stateLookingForBlocks(states *previousState):states(previousState)
{
    name = "State looking for cubes";
    startTimeState =getTimeMicroseconds();
    myPrivateState = wallFollowing;
    std::cout<<"looking for blocks";
}

void stateLookingForBlocks::processData(){
    startProcessData();
    long long int difTime = (getTimeMicroseconds()-startTimeState)/1000;
    //turnNDegreesSlowly(135);
    //std::cout<<"state: looking for blocks"<<std::endl;
    std::cout<<myPrivateState<<std::endl;
    
    switch(myPrivateState){
        case (wallFollowing):
            wallFollow();
            if(difTime > LOOKING_FOR_BLOCKS_STOP_AND_LOOK_TIME_MS){
                myPrivateState=looking;
            }
            break;
    case(looking):
        turnNDegreesSlowly(135);
        if(finishedTurningNDegreesSlowly){
            myPrivateState = comingBack;
        }
        break;
    case(comingBack):
        turnNDegreesSlowly(-135);
        if(finishedTurningNDegreesSlowly){
            myPrivateState = wallFollowing;
            startTimeState =getTimeMicroseconds();

        }
        break;
    }
    if(detectedCube()){
        nextState = new stateCollectingCube(this);
    }
    else if(foundCube()){
        nextState=new stateApproachBlock(this);
    }
    
    finishProcessData();
}
stateLookingForBlocks::~stateLookingForBlocks(){

}
