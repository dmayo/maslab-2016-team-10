#include "actuator.h"
#include <unistd.h>
#include <iostream>

actuator::actuator():
    rightWheel("right"),
    leftWheel("left"),
    sortServo("sort"),
    armServo("arm"),
    //hookServo(HOOK_SERVO_PWM),
    rightWheelPower(NULL),
    leftWheelPower(NULL),
    armServoAngle(NULL),
    //hookServoAngle(NULL),
    sortServoAngle(NULL),
    sensorsPointer(NULL){

    running=1;
    runThread = new std::thread(run,this);
    std::cout<<"actuator initialized"<<std::endl;

}

actuator::actuator(motorsControl &mymotorsControl, servosControl &myservosControl):actuator()
    {
    rightWheelPower = &mymotorsControl.rightMotorPower;
    leftWheelPower = &mymotorsControl.leftMotorPower;
    armServoAngle = &myservosControl.armAngle;
    //hookServoAngle = &myservosControl.hookAngle;
    sortServoAngle = &myservosControl.sortAngle;

}
//The actuator should receive an instance of sensors, so it can update the dir pin
// of the encoder. //OBSOLETE
actuator::actuator(sensorsModule * sensors):actuator()
{
    sensorsPointer= sensors;
    //It starts its own thread responsible for writting to the motors and servos.

}
actuator::~actuator(){
    running=0;
    runThread->join();
    delete runThread;
}

void actuator::run(actuator * myactuator){
    std::cout<<"actuator running"<<std::endl;
    //Here we see for each of the powers/angles if they have been defined
    //i.e. they point to a value
    // if they do, we update the things.
    while (myactuator->running){
        if (myactuator->rightWheelPower)
            myactuator->setPowerRightWheel(*(myactuator->rightWheelPower));
        if (myactuator->leftWheelPower)
            myactuator->setPowerLeftWheel(*(myactuator->leftWheelPower));
        if (myactuator->armServoAngle)
           myactuator->setArmServoAngle(*(myactuator->armServoAngle));
        /*
        if (myactuator->hookServoAngle)
            myactuator->setHookServoAngle(*(myactuator->hookServoAngle));
        */
        if (myactuator->sortServoAngle)
            myactuator->setSortServoAngle(*(myactuator->sortServoAngle));
        usleep(UPDATE_RATE_ACTUATORS_MILISECONDS * 1000);
    }

}


void actuator::setPowerLeftWheel(double speed){
    int dir;
    int encoderDir;
    if (speed >=0){
        encoderDir=0;
        dir =MOTOR_DIRECTION_FRONT;
    } else {
        encoderDir=1;
        dir =MOTOR_DIRECTION_BACK;
        speed=-speed;
    }

#if LEFT_ENCODER
    if(sensorsPointer){
        sensorsPointer->leftEncoder.dir =encoderDir;
    }
#endif

    speed = speed>1? 1: speed; //If speed >1, speed =1.
    speed= speed * MAXIMUM_NORMALIZED_SAFE_SPEED_MOTORS;
    leftWheel.setSpeed(speed,dir);
}

void actuator::setPowerRightWheel(double speed){
    int dir;
    int encoderDir;
#if MOTORS_OPPOSITE
    if (speed >=0){
        dir =MOTOR_DIRECTION_BACK;
        encoderDir=0;
    } else {
        encoderDir=1;
        dir =MOTOR_DIRECTION_FRONT;
        speed=-speed;
    }
#else
    if (speed >=0){
        encoderDir=0;
        dir =MOTOR_DIRECTION_FRONT;
    } else {
        encoderDir=1;
        dir =MOTOR_DIRECTION_BACK;
        speed=-speed;
    }
#endif

#if RIGHT_ENCODER
    if(sensorsPointer){
        sensorsPointer->rightEncoder.dir =encoderDir;
    }
#endif
    speed = speed>1? 1: speed; //If speed >1, speed =1.
    speed= speed * MAXIMUM_NORMALIZED_SAFE_SPEED_MOTORS;
    rightWheel.setSpeed(speed,dir);
}

void actuator::setSortServoAngle(double angle){
    double duty = angle/180.0;
    sortServo.moveServo(duty);

}

double actuator::getSortServoAngle(){
    if (sortServoAngle){
    return *sortServoAngle;}
    return -1;
}

void actuator::setArmServoAngle(double angle){
    double duty = angle/180.0;
    armServo.moveServo(duty);

}

double actuator::getArmServoAngle(){
    if (armServoAngle){
    return *armServoAngle;}
    return -1;
}
/*
void actuator::setHookServoAngle(double angle){
    double duty = angle/180.0;
    pwm.setServoPosition(hookServo.servoIndex,duty);

}

double actuator::getHookServoAngle(){
    if (hookServoAngle){
    return *hookServoAngle;}
    return -1;
}
*/

//void actuator::getRGData(int *r,int *g){
//    pwm.writePWM(myColorSensor.redPWM, .9);
//    usleep(100);
//    *r = myColorSensor.data_aio->read();
//    pwm.writePWM(myColorSensor.greenPWM,.9);
//    usleep(100);
//    *g = myColorSensor.data_aio->read();
//}
