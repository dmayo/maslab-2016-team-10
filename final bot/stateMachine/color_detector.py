from tamproxy.devices import Color

class ColorDetector(Color):

	def __init__(self, tamp, integrationTime=Color.INTEGRATION_TIME_101MS,gain=Color.GAIN_1X):
		super(self.__class__, self).__init__(tamp, integrationTime, gain)
		self.rb = 0
		self.gb = 0

	def getBlockColor(self):
            self.rb = (self.color.r+self.color.b)/2.
            self.gb = (self.color.g+self.color.b)/2.

            r2g = self.color.r/(self.gb+1)
            g2r = self.color.g/(self.rb+1)

            print "r2g" + str(r2g)
            print "g2r" + str(g2r)
            
            if r2g > 2 and g2r < 1:
                return "RED"
            elif g2r > 1 and r2g < 1:
                return "GREEN"
            else:
                return "NONE"
