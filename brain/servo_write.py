from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Servo


class ServoWrite(Sketch):
    """Cycles a servo back and forth between 0 and 180 degrees. However,
    these degrees are not guaranteed accurate, and each servo's range of valid
    microsecond pulses is different"""

    SERVO_PIN = 9

    def setup(self):
        self.servo = Servo(self.tamp, self.SERVO_PIN)
        self.servo.write(20)
        self.servoval = 20
        self.delta = 1
        self.timer = Timer()
        self.end = False

    def loop(self):
        if (self.timer.millis() > 10):
            self.timer.reset()
            if self.servoval >= 170: 
                self.delta = -2 # down
            elif self.servoval <= 20: 

                self.delta = 2 # up
            self.servoval += self.delta

            print self.servoval
            self.servo.write(abs(self.servoval))

if __name__ == "__main__":
    sketch = ServoWrite()
    sketch.run()
