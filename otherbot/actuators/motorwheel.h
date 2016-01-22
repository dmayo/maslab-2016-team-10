#ifndef MOTORWHEEL_H
#define MOTORWHEEL_H
#include <string>

class motorWheel
{
public:
    motorWheel(std::string wheelType);
    void setSpeed(double speed, double dir);
private:

};

#endif // MOTORWHEEL_H
