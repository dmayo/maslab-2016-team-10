from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Color
import pygame
from random import random

pygame.init()

# Prints RGB, clear(C), colorTemp, and lux values read and
# computed from the device. For more details, see the Adafruit_TCS34725
# Arduino library, from which the colorTemp and lux computations are
# used.

# Color sensor should be connected to the I2C ports (SDA and SCL)

def distance(x, y, z):
    a = (x-y)**2
    b = (x-z)**2
    c = (y-z)**2
    return ((a+b)**.5, (a+c)**.5, (b+c)**.5)



class ColorRead(SyncedSketch):

    def setup(self):

        self.screen = pygame.display.set_mode((300, 300))

        print 'Made it'
        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.timer = Timer()

        self.max_g = 0
        self.min_g = 255
        self.max_r = 0
        self.min_r = 255
    def loop(self):
        if self.timer.millis() > 100:
            events = pygame.event.get()

            self.screen.fill((0, 0, 0))

            self.timer.reset()
            # print self.color.r, self.color.g, self.color.b, self.color.c
            # print self.color.colorTemp, self.color.lux

            color_sum = (self.color.r**2 + self.color.g**2 + self.color.b**2+1)**.5

            r, g, b = 255*self.color.r/color_sum, 255*self.color.g/color_sum, 255*self.color.b/color_sum
            c = min(255*self.color.c/1000, 255)

            print 'Red: ' + str(self.color.r) + '\tGreen: ' + str(self.color.g) + '\tBlue: ' + str(self.color.b) 
            print 'Opacity: ' + str(self.color.c)
            print distance(r, g, b)

            self.screen.fill(((self.color.c > 500 and self.color.r > self.color.g)*255, (self.color.c > 500 and self.color.g > self.color.r)*255, 0))
            pygame.display.flip()



if __name__ == "__main__":
    sketch = ColorRead(1, -0.00001, 100)
    sketch.run()
