from tamproxy.devices import Gyro

class GyroWrap:
	def __init__(self,tamp):
		self.tamp=tamp
		self.ss_pin = 10 #gyro select pin
		self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
		self.initAngle = self.gyro.val
		self.newAngle = 0
		self.blockAngle = 0
		self.blockDistance = 0
		print "initial angle:"+str(self.initAngle)

		self.prevGyro = 0
		self.drift = -.02875
		self.totalDrift = 0
		self.gyroCAngle = 0

	def update(self):
		self.gyroCAngle=self.gyro.val - self.totalDrift #corrected angle
		# print (self.gyro.val-self.prevGyro), self.gyro.val, self.gyro.status, cAngle, self.totalDrift
		self.prevGyro=self.gyro.val
		self.totalDrift+=self.drift