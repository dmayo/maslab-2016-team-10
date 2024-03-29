from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor
from tamproxy.devices import Gyro
from tamproxy.devices import Encoder
from tamproxy.devices import Servo
from tamproxy.devices import Color
from tamproxy.devices import DigitalInput

import time

from random import random

from PID import PID
import os
import cv2
import time

import pygame


class PIDDrive(SyncedSketch):

    ss_pin = 10 #gyro select pin

    image_pipe = './image'
    if not os.path.exists(image_pipe):
        os.mkfifo(image_pipe)

    image_fd = os.open(image_pipe, os.O_RDONLY)

    def setup(self):
        #Pygame stuff
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))

        self.TicpIn = 4480/2.875

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
        

        self.prevGyro = 0
        self.drift = -.02875
        self.totalDrift = 0

        self.drifts = []
        
        
        self.PID=PID(.5, 1, 0.15)

        self.fwdVel = 0
        self.turnVel = 0
        self.turn = 0
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

        message = os.read(self.image_fd, 20)
        if message:
            # print("Recieved: '%s'" % message)
            if message[:2] == 'no':
                self.blockAngle = 0
                if self.State == 0:
                    self.State = 1

                if self.State == 2:
                    self.State = 3
            else:
                if self.State != 0:
                    self.State = 2
                try:
                    self.blockDistance, self.blockAngle = [number[:6] for number in message.split(',')]
                except:
                    self.blockAngle = 0
        self.blockAngle = float(self.blockAngle)
        if self.timer.millis() > 100:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.turnVel = -10
                    if event.key == pygame.K_RIGHT:
                        self.turnVel = 10

                    if event.key == pygame.K_UP:
                        self.fwdVel = 100
                    if event.key == pygame.K_DOWN:
                        self.fwdVel = -100

                    if event.key == pygame.K_1:
                        self.Sort = 1
                    if event.key == pygame.K_2:
                        self.Sort = 2

                    if event.key == pygame.K_SPACE:
                        self.MoveArm = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.turnVel = 0
                        self.turn = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.fwdVel = 0

            print 'Color'
            print self.color.c
            print self.color.r, self.color.g
            print 
            if self.color.c > 800 and self.Sort == 0:
                if self.color.r > self.color.g:
                    self.Sort = 1
                else:
                    self.Sort = 2

            # print self.uIR.val 
            if self.uIR.val == 0:
                self.MoveArm = True
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

            self.turn += self.turnVel


            self.timer.reset()
            #response = self.rp.read()
            #print "Got response %s" % response
            
            # Valid gyro status is [0,1], see datasheet on ST1:ST0 bits

            cAngle=self.gyro.val - self.totalDrift #corrected angle
            # print (self.gyro.val-self.prevGyro), self.gyro.val, self.gyro.status, cAngle, self.totalDrift
            self.prevGyro=self.gyro.val
            self.totalDrift+=self.drift


            # print 'State: ' + str(self.Searching)

            self.newAngle = cAngle + self.blockAngle
            print self.blockAngle

            pidResult=self.PID.valuePID(cAngle, cAngle+self.blockAngle+self.turn)
            

            # print 'Angle Dif: ' + str(cAngle-self.initAngle) + '\tPID RESULT: '+ str(pidResult)
            # print 'Encoders:\tR: ' + str(self.encoderR.val) + '\tL: ' + str(self.encoderL.val)
            # print 'AVG: ' + str((self.encoderR.val + self.encoderL.val)/2.)

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