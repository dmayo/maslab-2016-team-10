#include "stackbot.h"
int main(int argc, char** argv){
  stackbot mystackbot;
  //if no parameter was passed
  if (argc==1){
      mystackbot.running=1;
      mystackbot.run();

  }
  else{
      mystackbot.run(argc, argv);
  }
 
  return 0;
}


