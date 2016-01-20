from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor
from tamproxy.devices import Gyro
from PID import PID
import os
import cv2
import time

class PIDDrive(SyncedSketch):

    ss_pin = 10 #gyro select pin

    def setup(self):
              
        #motor left
        self.motorL = Motor(self.tamp, 2, 4)
        self.motorL.write(1,0)
        #self.deltaL = 1
        #self.motorvalL = 0
        
        #motor right
        self.motorR = Motor(self.tamp, 1, 3)
        self.motorR.write(1,0)
        #self.deltaR = 1
        #self.motorvalR = 0
        
        #gyro
        
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.initAngle=self.gyro.val
        print "initial angle:"+str(self.initAngle)
        

        self.prevGyro=0
        self.drift=-.027
        self.totalDrift=0
        
        
        self.PID=PID(1,0,0)

        self.fwdVel=0
        
        self.timer = Timer()
        '''
        self.pipePath = "./vision"
        print "ok1"
        time.sleep(1)
        try:
            os.mkfifo(self.pipePath)
        except OSError:
            print "error"
        print "ok"
        self.rp = open(self.pipePath, 'r')
        '''

    def loop(self):
        
        if self.timer.millis() > 100:
            self.timer.reset()
            response = self.rp.read()
            print "Got response %s" % response
            
            # Valid gyro status is [0,1], see datasheet on ST1:ST0 bits
            cAngle=self.gyro.val-self.totalDrift #corrected angle
            #print (self.gyro.val-self.prevGyro), self.gyro.val, self.gyro.status, cAngle, self.totalDrift
            self.prevGyro=self.gyro.val
            self.totalDrift+=self.drift

            pidResult=self.PID.valuePID(cAngle, self.initAngle)
            print (cAngle-self.initAngle), pidResult
            if(pidResult<=0):
                dirR=1
                dirL=0
            elif(pidResult>0):
                dirR=0
                dirL=1

            self.motorL.write(dirL,abs(pidResult))
            self.motorR.write(dirR,abs(pidResult))
            '''
            print "ok"
            #response = self.rp.read()
            #print "Got response %s" % response
            '''
            
if __name__ == "__main__":
    sketch = PIDDrive(1, -0.00001, 100)
    sketch.run()