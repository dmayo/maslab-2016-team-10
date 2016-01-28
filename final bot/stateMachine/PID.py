class PID:
	def __init__(self,kp,ki,kd):
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.errorOld=0
		self.timeInterval=0.1
		self.I=0

	def valuePID(self,actualValue, desiredValue):
		P = error = desiredValue - actualValue
		D=(error-self.errorOld)/self.timeInterval
		self.I+=error*self.timeInterval
		if(D<-5.0):
			self.I=0
		self.errorOld=error
		return self.kp*P+ self.ki*self.I+ self.kd*D