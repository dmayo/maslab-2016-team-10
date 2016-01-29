from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Servo

import pygame


class ServoWrite(Sketch):
    """Cycles a servo back and forth between 0 and 180 degrees. However,
    these degrees are not guaranteed accurate, and each servo's range of valid
    microsecond pulses is different"""

    SERVO_PIN = 9

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))

        self.servo = Servo(self.tamp, self.SERVO_PIN)
        self.servo.write(0)
        self.servoval = 0
        self.delta = 1
        self.timer = Timer()
        self.end = False
        self.wait = False



    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.servoval = 180
                if event.key == pygame.K_DOWN:
                    self.servoval = 0
                if event.key == pygame.K_SPACE:
                    self.servoval = 90
        if (self.timer.millis() > 10):
            self.timer.reset()
            if self.servoval >= 180: 
                self.delta = -1 # down
            elif self.servoval <= 0:
                self.delta = 1 # up
            elif self.wait == True:
                self.delta = 0
            # self.servoval += self.delta

            print self.servoval
            self.servo.write(abs(self.servoval))

if __name__ == "__main__":
    sketch = ServoWrite()
    sketch.run()
