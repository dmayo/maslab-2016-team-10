from tamproxy.devices import Encoder
from tamproxy.devices import Color
from tamproxy.devices import DigitalInput
from camera import Camera
from ir_array import Ir_array
from gyroWrap import GyroWrap

class Sensors:
    def __init__(self, tamp):
        self.tamp=tamp
		#color sensor
        self.color = Color(self.tamp,integrationTime=Color.INTEGRATION_TIME_101MS,gain=Color.GAIN_1X)

        #ultra IR pick up block detector
        self.uIR = DigitalInput(self.tamp, 17)
        self.uIR.val = 1

        #ir sensors
        self.irArray = Ir_array(self.tamp, 16, 15, 14, 40, 11, 10)

        #encoders
        self.encoderL = Encoder(self.tamp, 22, 23)
        self.encoderR = Encoder(self.tamp, 21, 20)

        #gyro
        self.gyro=GyroWrap(self.tamp)

        self.camera=Camera()

    #updates sensors except for the camera
    def update(self):
        self.gyro.update()