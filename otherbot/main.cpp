#include "cocoabot.h"
#include <iostream>
int main(int argc, char** argv){
  cocoabot mycocoabot;
  

  std::cout<<"main started"<<std::endl;
  //if no parameter was passed
  if (argc==1){
      mycocoabot.running=1;
      std::cout<<"no args"<<std::endl;
      mycocoabot.run();

  }
  else{
      //mycocoabot.run(argc, argv);
  }
 
  return 0;
}


