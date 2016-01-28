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
	myfifo = "./../brain/robot";
    /* create the FIFO (named pipe) */
    mkfifo(myfifo, 0666);

    delay_microsec=100000;
    this->wheelType=wheelType;

}

void motorWheel::setSpeed(double speed, double dir){
	//more pipes here
	std::cout << "speed " << speed << " dir " << dir << std::endl;

	std::string s = std::to_string(speed);

	// Cstring:
	char digits[5];
	std::strcpy( digits, wheelType.c_str() );
	/* write to the FIFO */
    fd = open(myfifo, O_WRONLY);
    write(fd, digits, sizeof(digits));

    close(fd);
    usleep(delay_microsec);
    /* remove the FIFO */
    //unlink(myfifo);
	std::cout<<"wrote"<<std::endl;
}