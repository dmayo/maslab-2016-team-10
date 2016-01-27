from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import AnalogInput
from ir_sensor import *
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

    adc_pin = 14
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    v_max = 1
    points = []
    distances = [[x, []] for x in xrange(2, 16)]
    distances = dict(distances)
    data = []
    set = 0

    def setup(self):
        self.test_sensor = Ir_sensor(self.tamp, self.adc_pin)
        # self.testpin = AnalogInput(self.tamp, self.adc_pin) #these
        self.timer = Timer() #this, too.

    def loop(self):
        if self.timer.millis() > 100:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        self.set = 2
                    if event.key == pygame.K_3:
                        self.set = 3
                    if event.key == pygame.K_4:
                        self.set = 4
                    if event.key == pygame.K_5:
                        self.set = 5
                    if event.key == pygame.K_6:
                        self.set = 6
                    if event.key == pygame.K_7:
                        self.set = 7
                    if event.key == pygame.K_8:
                        self.set = 8
                    if event.key == pygame.K_9:
                        self.set = 9
                    if event.key == pygame.K_a:
                        self.set = 10
                    if event.key == pygame.K_b:
                        self.set = 11
                    if event.key == pygame.K_c:
                        self.set = 12
                    if event.key == pygame.K_d:
                        self.set = 13
                    if event.key == pygame.K_e:
                        self.set = 14
                    if event.key == pygame.K_f:
                        self.set = 15
                    if event.key == pygame.K_SPACE:
                        self.data = []
                        for distance in self.distances:
                            self.data.append([1./distance, avg(self.distances[distance])])
                        for point in self.data:
                            for value in point:
                                print value, 
                            print

                if event.type == pygame.KEYUP:
                    self.set = 0

            self.timer.reset()

            v = self.test_sensor.get_distance()

            print 'Short: ' + str(self.test_sensor.get_distance())
            if self.set:
                self.distances[self.set].append(v)
            self.screen.fill((0, 0, 0))
            self.v_max = max(v, self.v_max)
            self.points.append(v)
            while len(self.points) > 60:
                self.points.pop(0)
            for x in xrange(len(self.points)):
                pygame.draw.rect(self.screen, (255, 255, 255), (x*5, 300-255*self.points[x]/self.v_max, 5, 5))
            for x in xrange(2, 16):
                y = 300-255*avg(self.distances[x])/self.v_max
                pygame.draw.rect(self.screen, (255, 0, 0), (600/x, y, 5, 5))

            pygame.display.flip()
if __name__ == "__main__":
    sketch = AnalogRead(1, -0.00001, 100)
    sketch.run()