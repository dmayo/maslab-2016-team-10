#ifndef SERVO_H
#define SERVO_H
#include <string>

class servo
{
public:
	std::string servoName;
    servo(std::string servoName);
    void moveServo(double duty);
};

#endif // SERVO_H
