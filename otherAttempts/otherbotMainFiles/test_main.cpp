#include <cstdio>
#include <cstring>
#include <stdlib.h>     /* atoi */
#include "imageProcessing/ImageProcessor.h"
#include <signal.h>
#include <sys/time.h>
#include  <thread>
#include <cmath>


int main( int, char** argv) {
    ImageProcessor myImageProcessor;
    myImageProcessor.run(&myImageProcessor);
    bool DEBUG=true;
    printf("something worked");
}

