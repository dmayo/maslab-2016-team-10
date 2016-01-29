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




class ColorRead(SyncedSketch):

    def setup(self):

        self.screen = pygame.display.set_mode((300, 300))

        print 'Made it'
        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.timer = Timer()

        self.max_r = 1
        self.max_g = 1
        self.max_b = 1
        self.max_temp = 1
        self.max_lux = 1
        self.max_opacity = 1
        self.max_dif = 1
        self.max_rb_dif = 1
        self.max_gb_dif = 1
        self.rb = 1
        self.gb = 1
        self.r_values = []
        self.g_values = []

    def loop(self):
        if self.timer.millis() > 100:


            self.screen.fill((0, 0, 0))

            self.timer.reset()
            # print self.color.r, self.color.g, self.color.b, self.color.c
            # print self.color.colorTemp, self.color.lux

            color_sum = (self.color.r**2 + self.color.g**2 + self.color.b**2 +.001)**.5

            r, g, b = 255*self.color.r/color_sum, 255*self.color.g/color_sum, 255*self.color.b/color_sum
            c = min(255*self.color.c/1000, 255)


            self.max_temp = max(self.max_temp, self.color.colorTemp)
            self.max_lux = max(self.max_lux, self.color.lux)
            self.max_opacity = max(self.max_opacity, self.color.c)



            maxes = [1, 1, 1, self.max_temp, self.max_lux, self.max_opacity, self.max_dif]


            temp = 255*self.color.colorTemp/self.max_temp
            lux = 255*self.color.lux/self.max_lux
            opacity = 255*self.color.c/self.max_opacity
            dif = (r-g)**2
            rb_dif = (r-b)**2
            gb_dif = (g-b)**2

            self.max_dif = max(self.max_dif, dif)
            self.max_rb_dif = max(self.max_rb_dif, rb_dif)
            self.max_gb_dif = max(self.max_gb_dif, gb_dif)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.r_values = [r, g, b, self.color.colorTemp, self.color.lux, self.color.c, dif]
                    if event.key == pygame.K_g:
                        self.g_values = [r, g, b, self.color.colorTemp, self.color.lux, self.color.c, dif]
            if self.r_values:
                for x in xrange(len(self.r_values)):
                    pygame.draw.rect(self.screen, (255, 0, 0), (10+10*x+1, 300-[1, 255][x > 2]*self.r_values[x]/maxes[x]-5, 2, 12))
            if self.g_values:
                for x in xrange(len(self.g_values)):
                    pygame.draw.rect(self.screen, (0, 255, 0), (10+10*x+1, 300-[1, 255][x > 2]*self.g_values[x]/maxes[x]-5, 2, 12))

            # self.screen.fill(((self.color.r > 400 and self.color.r > self.color.g)*255, (self.color.g > 400  and self.color.g > self.color.r)*255, 0))

            pygame.draw.rect(self.screen, (255, 0, 0), (10, 300-r, 5, 5))
            pygame.draw.rect(self.screen, (0, 255, 0), (20, 300-g, 5, 5))
            pygame.draw.rect(self.screen, (0, 0, 255), (30, 300-b, 5, 5))
            
            pygame.draw.rect(self.screen, (255, 255, 0), (50, 300-temp, 5, 5))
            pygame.draw.rect(self.screen, (0, 255, 255), (60, 300-lux, 5, 5))
            pygame.draw.rect(self.screen, (255, 0, 255), (70, 300-opacity, 5, 5))
            
            pygame.draw.rect(self.screen, (255, 255, 255), (90, 300-255*dif/self.max_dif, 5, 5))

            pygame.draw.rect(self.screen, (255, 0, 255), (110, 300-255*rb_dif/self.max_rb_dif, 5, 5))
            pygame.draw.rect(self.screen, (0, 255, 255), (120, 300-255*gb_dif/self.max_gb_dif, 5, 5))

            self.rb = (self.color.r+self.color.b)/2.
            self.gb = (self.color.g+self.color.b)/2.

            r2g = self.color.r/(self.gb+1)
            g2r = self.color.g/(self.rb+1)

            print "r2g" + str(r2g)
            print "g2r" + str(g2r)
            
            if r2g > 2 and g2r < 1:
                self.screen.fill((255, 0, 0))
            elif g2r > 1 and r2g < 1:
                self.screen.fill((0, 255, 0))
            else:
                self.screen.fill((0, 0, 0))

            pygame.display.flip()



if __name__ == "__main__":
    sketch = ColorRead(1, -0.00001, 100)
    sketch.run()
