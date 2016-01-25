#include "motorwheel.h"
#include <string>
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sstream>
#include <sys/stat.h>
#include <sys/types.h>

motorWheel::motorWheel(std::string wheelType)
{
    //named pipes goes here

}

void motorWheel::setSpeed(double speed, double dir){
	//more pipes here
	std::cout << "speed " << speed << " dir " << dir << std::endl;
	int fd;
	std::ostringstream strm;
	char const* namedPipe = "./motorL";
	mkfifo(namedPipe, 0666);
	fd = open(namedPipe, O_WRONLY | O_NONBLOCK);
	std::string numStr = strm.str();
	const char* cstr1 = numStr.c_str();
	write(fd, cstr1, sizeof(cstr1));
	close(fd);
	std::cout<<"wrote"<<std::endl;
}