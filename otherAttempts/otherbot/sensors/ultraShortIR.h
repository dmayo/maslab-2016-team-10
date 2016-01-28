#ifndef ULTRASHORTIR_H
#define ULTRASHORTIR_H
#include "sensorssuperclass.h"

class ultraShortIR: public sensorsSuperClass
{
  public:
    	//mraa::Gpio * data_gpio;
	ultraShortIR(int dataPin);
        int readData();
        double getData();
    private:
    	int myDataPin;

    
};


#endif
