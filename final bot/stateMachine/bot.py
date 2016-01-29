from tamproxy import Sketch, SyncedSketch, Timer

import time

from startState import startState
from sensors import Sensors
from actuators import Actuators
from utils import Utils
from motorController import MotorController

class Bot(SyncedSketch):

    def setup(self):
        self.timer = Timer()
        self.utils = Utils(time.time(),180) #start time, total game time
        self.sensors = Sensors(self.tamp)
        self.actuators = Actuators(self.tamp)
        self.motorController= MotorController(self.sensors,self.actuators)
        self.myState = startState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

    def loop(self):
        try:
            self.myState=self.myState.run() #run current state and return next state
        except KeyboardInterrupt:
            raise
        except:
            print "cought an error, back to start state"
            self.myState=startState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

        self.timer.reset()
            
if __name__ == "__main__":
    sketch = Bot(1, -0.00001, 100)
    sketch.run()