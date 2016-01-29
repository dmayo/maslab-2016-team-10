from tamproxy.devices import Color

class ColorDetector:
	def __init__(self, tamp):
		self.r2g = 0
		self.g2r = 0
		self.tamp=tamp
		self.color = Color(self.tamp,integrationTime=Color.INTEGRATION_TIME_101MS,gain=Color.GAIN_1X)

	def getBlockColor(self):
		""" Returns 'GREEN', 'RED' or 'NONE'"""
		self.rb = (self.color.r+self.color.b)/2.
		self.gb = (self.color.g+self.color.b)/2.

		r2g = self.color.r/(self.gb+1)
		g2r = self.color.g/(self.rb+1)

		#print "r2g" + str(r2g)
		#print "g2r" + str(g2r)

		if r2g > 1.5 and g2r < 1:
			return "Red"
		elif g2r > 1 and r2g < 1:
			return "Green"
		else:
			return "None"