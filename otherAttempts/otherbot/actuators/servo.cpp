#include "servo.h"
#include <iostream>

servo::servo(std::string servoName)
{
	this->servoName = servoName;
	//use servoName as pipe name
}

void servo::moveServo(double duty){
	//pipes here
	//std::cout << servoName << " " << duty;
}

