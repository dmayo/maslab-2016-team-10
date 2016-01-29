from tamproxy.devices import Color
from color_detector import ColorDetector
from tamproxy.devices import DigitalInput
from color_detector import ColorDetector
from camera import Camera
from ir_array import Ir_array
from gyroWrap import GyroWrap
from encoderWrap import EncoderWrap

class Sensors:
    def __init__(self, tamp):
        self.tamp=tamp
		#color sensor
        self.color = ColorDetector(self.tamp)

        #ultra IR pick up block detector
        self.uIR = DigitalInput(self.tamp, 17)
        self.uIR.val = 1

        self.button = DigitalInput(self.tamp, 8)
        self.button.val = 0

        #ir sensors
        self.irArray = Ir_array(self.tamp, 16, 15, 14, 40, 11, 10)

        #encoders
        self.encoders=EncoderWrap(self.tamp)

        #gyro
        self.gyro=GyroWrap(self.tamp)

        self.camera=Camera()

    #updates all sensors except for the camera
    def update(self):
        self.irArray.update()
        self.encoders.update()
        self.gyro.update()

