from tamproxy.devices import Gyro
from tamproxy.devices import Encoder
from tamproxy.devices import Color
from tamproxy.devices import DigitalInput
from camera import Camera
from ir_array import Ir_array

class Sensors:
    def __init__(self, tamp):
        self.tamp=tamp
		#color sensor
        self.color = Color(self.tamp,integrationTime=Color.INTEGRATION_TIME_101MS,gain=Color.GAIN_1X)

        #ultra IR pick up block detector
        self.uIR = DigitalInput(self.tamp, 17)
        self.uIR.val = 1

        self.ir_array = Ir_array(self.tamp, 16, 15, 14, 40, 11, 10)

        #encoders
        self.encoderL = Encoder(self.tamp, 22, 23)
        self.encoderR = Encoder(self.tamp, 21, 20)

        #gyro
        self.ss_pin = 10 #gyro select pin
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.initAngle = self.gyro.val
        self.newAngle = 0
        self.blockAngle = 0
        self.blockDistance = 0
        print "initial angle:"+str(self.initAngle)

        self.prevGyro = 0
        self.drift = -.02875
        self.totalDrift = 0
        self.gyroCAngle = 0

        self.camera=Camera()

    def updateGyro(self):
        self.gyroCAngle=self.gyro.val - self.totalDrift #corrected angle
        # print (self.gyro.val-self.prevGyro), self.gyro.val, self.gyro.status, cAngle, self.totalDrift
        self.prevGyro=self.gyro.val
        self.totalDrift+=self.drift


