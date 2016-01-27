import time
class Utils:
	def __init__(self, startTime, totalGameTime):
		self.startTime = startTime
		self.totalGameTime = totalGameTime #in seconds

	def gameTimeRemaining():
		return (self.startTime+(self.totalGameTime*10**-6))-time.time() #returns time remaining in microseconds

	def gameRunningTime():
		return time.time()-self.startTime

	def resetClock():
		self.startTime=time.time()
