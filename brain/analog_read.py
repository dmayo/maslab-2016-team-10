from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import AnalogInput
from ir_array import *
import pygame

# Reads the analog voltage at one of the analog pins

def avg(nums):
    if nums:
        return sum(nums)/len(nums)
    else:
        return 0

def Long(V):
    '''Min: 3in -- Max:24in '''
    return 1.818*10**5/(V-1779.07)
def Short(V):
    '''Min: 1.75in -- Max:12in'''
    return 1.0656*10**5/(V+633.328)

class AnalogRead(SyncedSketch):

    screen = pygame.display.set_mode((300, 300))

    v_max = 1
    points = []
    distances = [[x, []] for x in xrange(2, 16)]
    distances = dict(distances)
    data = []
    set = 0

    def setup(self):
        self.sensor_array = Ir_array(self.tamp, 16, 15, 14, 40, 11, 10)
        # self.testpin = AnalogInput(self.tamp, self.adc_pin) #these
        self.timer = Timer() #this, too.

    def loop(self):
        if self.timer.millis() > 100:
            self.screen.fill((0, 0, 0))
            events =  pygame.event.get()
            self.sensor_array.update()

            for x in xrange(6):
                value = self.sensor_array.ir_value[x]
                print value
                if value != float('inf'):
                    pygame.draw.rect(self.screen, (255, 255, 255), (10*x, 300-value*10, 5, 5))
            pygame.display.flip()


if __name__ == "__main__":
    sketch = AnalogRead(1, -0.00001, 100)
    sketch.run()