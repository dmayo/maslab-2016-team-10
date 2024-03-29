#include "stateapproachblock.h"
#include "statecollectingcube.h"
#include "stategoingtocube.h"
#include "statelookingforblocks.h"
stateApproachBlock::stateApproachBlock(states * previousState):states(previousState)
{
    name="approaching cube";
}

void stateApproachBlock::processData(){
    startProcessData();


    if(finishedFollowingPoint){
        nextState= new stateGoingToCube(this);
    }
    if(foundCube()){
        followPoint(getDistanceNearestCube(),getAngleNearestCube());
    }
    else{
        nextState= new stateLookingForBlocks(this);
    }
    finishProcessData();
}

stateApproachBlock::~stateApproachBlock(){

}
