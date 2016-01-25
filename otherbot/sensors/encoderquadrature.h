/*Based on the staff code.
 * It tells which directions the wheels are spinning by using the quadrature between the data in.
 *
 */
#ifndef ENCODERQUADRATURE_H
#define ENCODERQUADRATURE_H
#include "sensorssuperclass.h"
#include "../configFile.h"
#include <thread>
 #include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <iostream>
 #define MAX_BUF 1024

class encoderQuadrature : public sensorsSuperClass
{
public:
    encoderQuadrature(int encA, int encB, int isLeft);
    static void run(void* encoderQuadraturePointer);
    std::thread *runThread;
    //mraa::Gpio encAGpio;
    //mraa::Gpio encBGpio;

    static void aHandler(void * myEnc);
    static void bHandler(void * myEnc);
    int getPhase(int a, int b);
    void updateTick(int prevPhase, int curPhase);
    // Variables are volatile to ensure memory consistency between different
    // edge callbacks.

    long long getCounts();
    double getData();
    double getRotations();

    volatile int aState=0;
    volatile int bState=0;
    volatile int count = 0;

    int reversed; //+1 or -1
    int error;
    int dir; //for reverse compatibility, not used.
};

#endif // ENCODERQUADRATURE_H
