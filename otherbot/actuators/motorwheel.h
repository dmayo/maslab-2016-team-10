#ifndef MOTORWHEEL_H
#define MOTORWHEEL_H
#include <string>

class motorWheel
{
public:
    motorWheel(std::string wheelType);
    void setSpeed(double speed, double dir);
private:
	char * myfifo;
	int fd;
	unsigned int delay_microsec;
	std::string wheelType;
};

#endif // MOTORWHEEL_H
