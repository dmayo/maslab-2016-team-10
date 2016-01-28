#include "encoder.h"
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <iostream>
#define MAX_BUF 1024

encoder::encoder(int encPin)
 //encGpio(encPin), dir(0)
{
	edgeCount = 0;
	rotations = 0.0;
	running = 1;

//	dirGpio.dir(mraa::DIR_OUT);
    //encGpio.dir(mraa::DIR_IN);
	//encGpio.isr(mraa::EDGE_BOTH, edge_handler, this);
    runThread = new std::thread(run,this);
}

encoder::~encoder() {
	running = 0;
    runThread->join();
    delete runThread;
}

void encoder::run(void* encoderSensorPointer) {
	encoder* encSensor = (encoder*) encoderSensorPointer;
	while(1){
		std::cout<<"encoder running"<<std::endl;
	}
	/*

	int offset;
	// if dir is 1, then wheels are rotating backwards
    if (encSensor->dir == 1) {
		offset = -1;
	}
	// if dir is 0, then wheels are rotating forwards
	else {
		offset = 1;
	}
	*/
	/*
    int fd;
    char * myfifo = "./../brain/encoder";
    char buf[MAX_BUF];
    std::cout<<"works"<<std::endl;
    //open, read, and display the message from the FIFO
    fd = open(myfifo, O_RDONLY);
	while (1){
		std::cout<<"works2"<<std::endl;
		//encSensor->edgeCount = encSensor->edgeCount + offset;
		read(fd, buf, MAX_BUF);
		std::cout<<buf<<std::endl;
		encSensor->edgeCount = atof(buf); //get edge count from python
	}
	close(fd);
	*/

}


long long encoder::getCounts() {
	return edgeCount;
}

double encoder::getRotations() {
    float edgeCountFloat = edgeCount;
    rotations = (edgeCountFloat / EDGES_PER_ROTATION) / GEAR_RATIO;
	return rotations;
}

double encoder::getData(){
    return CIRCUMFERENCE_WHEEL*getRotations();
}
