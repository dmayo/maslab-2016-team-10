from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor
from tamproxy.devices import Gyro
from tamproxy.devices import Encoder
from PID import PID
import os
import cv2
import time

class PIDDrive(SyncedSketch):

    ss_pin = 10 #gyro select pin

    def setup(self):

        self.TicpIn = 4480/2.875

        self.encoderL = Encoder(self.tamp, 22, 23)
        self.encoderR = Encoder(self.tamp, 21, 20)

        self.init_time = time.time()
        # self.encoderL = Encoder(self.tamp, 23, 22)
        # self.encoderR = Encoder(self.tamp, 21, 20)

        #motor left
        self.motorL = Motor(self.tamp, 2, 4)
        self.motorLdrive = 0
        self.motorL.write(1,0)
        #self.deltaL = 1
        #self.motorvalL = 0
        
        #motor right
        self.motorR = Motor(self.tamp, 1, 3)
        self.motorRdrive = 0
        self.motorR.write(1,0)
        #self.deltaR = 1
        #self.motorvalR = 0

        #gyro
        
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.initAngle = self.gyro.val

        print "initial angle:"+str(self.initAngle)
        

        self.prevGyro = 0
        self.drift = -.02875
        self.totalDrift = 0

        self.drifts = []
        
        
        self.PID=PID(5,4,.2)

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
            #response = self.rp.read()
            #print "Got response %s" % response
            
            # Valid gyro status is [0,1], see datasheet on ST1:ST0 bits

            cAngle=self.gyro.val - self.totalDrift #corrected angle
            #print (self.gyro.val-self.prevGyro), self.gyro.val, self.gyro.status, cAngle, self.totalDrift
            self.prevGyro=self.gyro.val
            self.totalDrift+=self.drift


            pidResult=self.PID.valuePID(cAngle, self.initAngle)
            

            print 'Angle Dif: ' + str(cAngle-self.initAngle) + '\tPID RESULT: '+ str(pidResult)
            print 'Encoders:\tR: ' + str(self.encoderR.val) + '\tL: ' + str(self.encoderL.val)
            print 'AVG: ' + str((self.encoderR.val + self.encoderL.val)/2.)

            self.motorLdrive = self.fwdVel - pidResult
            self.motorRdrive = self.fwdVel + pidResult

            if self.motorLdrive >= 0:
                dirL = 0
            else:
                dirL = 1
            if self.motorRdrive >= 0:
                dirR = 0
            else:
                dirR = 1


            self.motorL.write(dirL,abs(self.motorLdrive))
            self.motorR.write(dirR,abs(self.motorRdrive))

            '''
            print "ok"
            #response = self.rp.read()
            #print "Got response %s" % response
            '''
            
if __name__ == "__main__":
    sketch = PIDDrive(1, -0.00001, 100)
    sketch.run()