from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor
from tamproxy.devices import Gyro
from tamproxy.devices import Encoder
from tamproxy.devices import Servo
from tamproxy.devices import Color
from tamproxy.devices import DigitalInput
from ir_array import *

import time

from random import random

from PID import PID
import os
import cv2
import time



class PIDDrive(SyncedSketch):

    ss_pin = 10 #gyro select pin

    # image_pipe = './image'
    # if not os.path.exists(image_pipe):
    #     os.mkfifo(image_pipe)

    # image_fd = os.open(image_pipe, os.O_RDONLY)

    def setup(self):



        self.TicpIn = 4480/2.875

        self.ir_array = Ir_array(self.tamp, 16, 15, 14, 40, 11, 10)

        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)

        self.uIR = DigitalInput(self.tamp, 17)
        self.uIR.val = 1

        self.servo = Servo(self.tamp, 9)
        self.servo.bottom = 0
        self.servo.top = 200
        self.servo.speed = 30
        self.servo.write(self.servo.bottom)
        self.servoval = self.servo.bottom
        self.delta = 0


        self.sorter = Servo(self.tamp, 5)
        self.sorter.center = 90
        self.sorter.right = 25
        self.sorter.left = 165
        self.sorter.speed = 15

        self.sorter.write(self.sorter.center)
        self.sorterval = self.sorter.center
        self.dsorter = 0

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
        self.motorR = Motor(self.tamp,1, 3)
        self.motorRdrive = 0
        self.motorR.write(1,0)
        #self.deltaR = 1
        #self.motorvalR = 0

        #gyro
        
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.initAngle = self.gyro.val
        self.newAngle = 0
        self.blockAngle = 0
        self.blockDistance = 0
        print "initial angle:"+str(self.initAngle)
        
        self.Follow = 'Right'
        self.IRs = {'Left': [0, 1, 2], 'Right': [5, 4, 3]}

        self.prevGyro = 0
        self.drift = -.02875
        self.totalDrift = 0

        self.drifts = []
        
        
        self.PID=PID(.5, 1, 0.15)
        self.IRPID = PID(10, 5, .15)

        self.fwdVel = 30
        self.turnVel = 0
        self.MoveArm, self.Top, self.Bottom = False, 0, 0

        self.Sort = 0
        self.SortPause = 0

        self.State = 1
        
        self.timer = Timer()



    def loop(self):
        #state 0 - wait for first no block, do nothing
            #transition: no block -> state 1
        #state 1 - look for block
            #transition: found block -> state 2
        #sate 2 - drive over block
            #transition: ir triggered -> state 3
        #sate 3 - pick up block
            #transition: color sensor done -> sate 1

        if self.timer.millis() > 100:
            

            print 'Color'
            print self.color.c
            print self.color.r, self.color.g
            if self.color.c > 800 and self.Sort == 0:
                if self.color.r > self.color.g:
                    self.Sort = 1
                else:
                    self.Sort = 2

            # print self.uIR.val 
            if self.uIR.val == 0:
                #  self.MoveArm = True
                self.State = 0

            if self.MoveArm:
                if self.Bottom == 2 and self.Top == 1:
                    self.delta = 0
                    self.servoval = self.servo.bottom
                    self.servo.write(self.servo.bottom)
                    self.Bottom, self.Top = 0, 0
                    self.MoveArm = False

                elif self.servoval >= self.servo.top: 
                    time.sleep(1)
                    self.delta = -self.servo.speed

                    self.Top = 1

                elif self.servoval <= self.servo.bottom: 
                    self.delta = self.servo.speed

                    self.Bottom = 1
                    if self.Top == 1:
                        self.Bottom = 2


            if self.Sort == 1:
                if self.sorterval < self.sorter.left:
                    self.dsorter = self.sorter.speed
                elif self.sorterval >= self.sorter.left:
                    self.dsorter = 0
                    self.Sort = 3
                    self.SortPause = time.time()

            if self.Sort == 2:
                if self.sorterval > self.sorter.right:
                    self.dsorter = -self.sorter.speed
                elif self.sorterval <= self.sorter.right:
                    self.dsorter = 0
                    self.Sort = 3
                    self.SortPause = time.time()

            if self.Sort == 3:
                if time.time() - self.SortPause > 1:
                    self.sorterval = self.sorter.center
                    self.Sort = 0


            self.sorterval += self.dsorter
            self.sorter.write(abs(self.sorterval))

            self.servoval += self.delta
            self.servo.write(abs(self.servoval))

            self.initAngle += self.turnVel


            self.timer.reset()
            #response = self.rp.read()
            #print "Got response %s" % response
            
            # Valid gyro status is [0,1], see datasheet on ST1:ST0 bits

            cAngle=self.gyro.val - self.totalDrift #corrected angle
            # print (self.gyro.val-self.prevGyro), self.gyro.val, self.gyro.status, cAngle, self.totalDrift
            self.prevGyro=self.gyro.val
            self.totalDrift+=self.drift

            # message = os.read(self.image_fd, 20)
            # if ParseMessage(message):
            #     self.blockDistance, self.blockAngle = ParseMessage(message)
        
            # print 'Angle Dif: ' + str(cAngle-self.initAngle) + '\tPID RESULT: '+ str(pidResult)
            # print 'Encoders:\tR: ' + str(self.encoderR.val) + '\tL: ' + str(self.encoderL.val)
            # print 'AVG: ' + str((self.encoderR.val + self.encoderL.val)/2.)



            self.ir_array.update()
            ir = self.ir_array.ir_value
            avg = (ir[self.IRs[self.Follow][0]]+.15+ir[self.IRs[self.Follow][1]]/2)/2
            min_val = min(ir[0], ir[1])

            if avg != float('inf'):
                pidResult= -self.IRPID.valuePID(4, avg)
            elif min_val != float('inf'):
                pidResult= -self.IRPID.valuePID(4, min_val)
            else:
                pidResult = -20

            if ir[self.IRs[self.Follow][2]] < 4:
                pidResult = 20
                self.fwdVel = 0
            else:
                self.fwdVel = 30
            print 'IR + ' + str(ir[self.IRs[self.Follow][0]]) +', ' + str(.15+ir[self.IRs[self.Follow][1]]/2)
            print 'AVG + ' + str(avg)
            print 'Min_Val + ' + str(min_val)
            print 'Front + ' + str(ir[self.IRs[self.Follow][2]])
            print 'Angle + ' + str(cAngle)
            print 'PID + ' + str(pidResult)

            self.motorLdrive = 0 # self.fwdVel - pidResult
            self.motorRdrive = 0 # self.fwdVel + pidResult
            print 'MotorL + ' + str(self.motorLdrive)
            print 'MotorR + ' + str(self.motorRdrive)
            self.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
            self.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

            '''
            print "ok"
            #response = self.rp.read()
            #print "Got response %s" % response
            '''

    def ParseMessage(message):
        if message:
            if message[:2] == 'no':
                blockDistance, blockAngle = 0, 0
                return None
            else:
                try:
                    blockDistance, blockAngle = [number[:6] for number in message.split(',')]
                except:
                    blockDistance, blockAngle = 0, 0
            return blockDistance, blockAngle
        else:
            return None
            
if __name__ == "__main__":
    sketch = PIDDrive(1, -0.00001, 100)
    sketch.run()