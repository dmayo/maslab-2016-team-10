#include "button.h"
#include <csignal>
#include <iostream>
#include <cmath>
#include <sys/time.h>
#include <unistd.h>

button::button(int Pin)
{
	/*
    data_gpio = new mraa::Gpio(Pin);
    if (data_gpio == NULL){
        return;
    }
    data_gpio->dir(mraa::DIR_IN);
	*/
    int myDataPin = Pin;
}
int button::readData(){
	return 0;
    //return data_gpio->read();
}
double button::getData(){
	return 0;
    //return readData();
}
