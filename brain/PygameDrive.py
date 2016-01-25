from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor
from tamproxy.devices import Gyro
from tamproxy.devices import Encoder
from tamproxy.devices import Servo
from tamproxy.devices import Color

import time

from PID import PID
import os
import cv2
import time

import pygame


class PIDDrive(SyncedSketch):

    ss_pin = 10 #gyro select pin

    def setup(self):
        #Pygame stuff
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))

        self.TicpIn = 4480/2.875

        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)

        self.servo = Servo(self.tamp, 9)
        self.servo.write(20)
        self.servoval = 20
        self.delta = 0


        self.sorter = Servo(self.tamp, 5)
        self.sorter.center = 98
        self.sorter.right = 20
        self.sorter.left = 170
        self.sorter.speed = 30

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

        print "initial angle:"+str(self.initAngle)
        

        self.prevGyro = 0
        self.drift = -.02875
        self.totalDrift = 0

        self.drifts = []
        
        
        self.PID=PID(5, 4, .15)

        self.fwdVel = 0
        self.turnVel = 0
        self.MoveArm, self.Top, self.Bottom = False, 0, 0

        self.Sort = 0
        self.SortPause = 0
        
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
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.turnVel = -5
                    if event.key == pygame.K_RIGHT:
                        self.turnVel = 5

                    if event.key == pygame.K_UP:
                        self.fwdVel = 100
                    if event.key == pygame.K_DOWN:
                        self.fwdVel = -100

                    if event.key == pygame.K_SPACE:
                        self.MoveArm = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.turnVel = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.fwdVel = 0
                        
            if self.color.c > 500 and self.Sort == 0:
                if self.color.r > self.color.g:
                    self.Sort = 1
                else:
                    self.Sort = 2

            if self.MoveArm:
                if self.Bottom == 2 and self.Top == 1:
                    self.delta = 0
                    self.servoval = 20
                    self.servo.write(20)
                    self.Bottom, self.Top = 0, 0
                    self.MoveArm = False

                elif self.servoval >= 175: 
                    self.delta = -30

                    self.Top = 1

                elif self.servoval <= 30: 
                    self.delta = 30

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


            pidResult=self.PID.valuePID(cAngle, self.initAngle)
            

            print 'Angle Dif: ' + str(cAngle-self.initAngle) + '\tPID RESULT: '+ str(pidResult)
            print 'Encoders:\tR: ' + str(self.encoderR.val) + '\tL: ' + str(self.encoderL.val)
            print 'AVG: ' + str((self.encoderR.val + self.encoderL.val)/2.)

            self.motorLdrive = self.fwdVel - pidResult
            self.motorRdrive = self.fwdVel + pidResult

            self.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
            self.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

            '''
            print "ok"
            #response = self.rp.read()
            #print "Got response %s" % response
            '''
            
if __name__ == "__main__":
    sketch = PIDDrive(1, -0.00001, 100)
    sketch.run()