#include "ultraShortIR.h"
#include <csignal>
#include <iostream>
#include <cmath>
#include <sys/time.h>
#include <unistd.h>


ultraShortIR::ultraShortIR(int dataPin){
	/*
  	data_gpio = new mraa::Gpio(dataPin);
	if (data_gpio == NULL){
		return;
	}

	data_gpio->dir(mraa::DIR_IN);
	*/

	int myDataPin = dataPin;
}

int ultraShortIR::readData(){
	//return data_gpio->read();
	return 0;
}

double ultraShortIR::getData(){
    return readData();
}

int run_ultraShortIRTest(){
	usleep(50000.0);
	ultraShortIR anUltraShortIR(2);
	while (true){
		usleep(50000.0);
		int reading = anUltraShortIR.getData();
		std::cout << reading << std::endl;
	}
}

