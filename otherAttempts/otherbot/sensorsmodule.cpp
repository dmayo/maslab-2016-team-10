#include "sensorsmodule.h"
#include <iostream>

sensorsModule::sensorsModule():
    //Here is the initializer. It defines initial values for all the variables and initializes all the objects

    rightEncoderMovement(0),
    leftEncoderMovement(0),
    encoderAngle(0),
    teamData(0),
    onData(0),
    gyroscopeAngle(0),
    gyroscopeReading(0),
    teamDataAlpha(0),
    onDataAlpha(0),
    encoderAlpha(ENCODER_ALPHA),
    encoderAngleAlpha(ENCODER_ANGLE_ALPHA),
    gyroscopeTotalAlpha(GYROSCOPE_TOTAL_ALPHA),
    gyroscopeReadingAlpha(GYROSCOPE_READING_ALPHA)


    #if LEFT_ENCODER
    ,leftEncoder(LEFT_ENCODER_ENC_A,LEFT_ENCODER_ENC_B,1)
    #endif
    #if RIGHT_ENCODER
    ,rightEncoder(RIGHT_ENCODER_ENC_A,RIGHT_ENCODER_ENC_B,1)
    #endif

    #if GYROSCOPE
    ,mygyroscope()
    #endif

    #if COLOR_DETECTOR
    ,colorSensor(COLOR_DETECTOR_PIN)
    #endif

{
    running=1;
    std::cout<<"sensors module initialized"<<std::endl;
    runThread = new std::thread(run,this);
}


sensorsModule::~sensorsModule(){
    running=0;
    runThread->join();
    delete runThread;
}


void sensorsModule::run(sensorsModule * sensors){
    std::cout<<"sensors module running"<<std::endl;
    int started =0;

    while (sensors->running){
        #if RIGHT_ENCODER
        updateSensor(&sensors->rightEncoder,&sensors->rightEncoderMovement, sensors->encoderAlpha,started);
        #endif

        #if LEFT_ENCODER
        updateSensor(&sensors->leftEncoder,&sensors->leftEncoderMovement, sensors->encoderAlpha,started);
        #endif
        #if RIGHT_ENCODER*LEFT_ENCODER
        double newEncoderAngle= (-sensors->rightEncoderMovement+sensors->leftEncoderMovement)/DISTANCE_DIFFERENCE_FOR_360_DEGREES*360;
        updateData(&sensors->encoderAngle,newEncoderAngle, sensors->encoderAngleAlpha,started);
        #endif

        updateTime(sensors);
        usleep(SENSORS_UPDATE_RATE_MILISECONDS);
        started=1;
    }

}

void sensorsModule::updateSensor(sensorsSuperClass *sensor, volatile double *data, float alpha, int started){
    //We want to have a time out here on the getData
    double newData = sensor->getData();
    updateData(data,newData,alpha,started);
}

void sensorsModule::updateData(volatile double *previousData, double newData, float alpha, int started){
    if (started){
        if (isinf(*previousData)){
            *previousData=newData;
        }
        else{
        *previousData = kalmanFilter(*previousData,newData, alpha);
        }
    }
    else{
        *previousData=newData;
    }
}

double sensorsModule::kalmanFilter(double previousData, double newData, float alpha){
    return (previousData*alpha + newData * (1-alpha));
}


void sensorsModule::updateTime(sensorsModule *sensors){
    sensors->timeMicrosecondsSinceEpoch = std::chrono::duration_cast<std::chrono::microseconds>
                (std::chrono::system_clock::now().time_since_epoch()).count(); //magic from Stack Overflow
}

double sensorsModule::getAngle(){
    if(USE_GIROSCOPE_FOR_ANGLE){
        return gyroscopeAngle;
    }
    else{
        return encoderAngle;
    }
}

double sensorsModule::getPosition(){
    return (rightEncoderMovement+leftEncoderMovement)/2;
}
