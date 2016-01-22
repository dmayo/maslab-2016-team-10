#include "shortIR.h"
#include <csignal>
#include <iostream>
#include <sys/time.h>

int runShortIR(){
  int reading;
	usleep(50000.0);
	shortIR aShortIR(2);
	reading = aShortIR.timing();
	std::cout << reading << std::endl;
}


