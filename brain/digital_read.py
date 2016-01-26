from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import DigitalInput

# Detects changes in allllll the pins!

class DigitalRead(SyncedSketch):

    def setup(self):
        self.testpins = []
        for i in xrange(34):
            self.testpins.append(DigitalInput(self.tamp, i))

    def loop(self):
        print 17, self.testpins[17].val

if __name__ == "__main__":
    sketch = DigitalRead(1, -0.00001, 100)
    sketch.run()