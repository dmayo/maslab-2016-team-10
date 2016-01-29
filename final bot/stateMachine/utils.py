import time
import timeout

class Utils:
	def __init__(self, startTime, totalGameTime):
		self.startTime = startTime
		self.totalGameTime = totalGameTime #in seconds
		self.isGameStarted=False
		self.navTimeout = timeout.Timeout(60) #timeout for navigation states, i.e. WallFollowingState and LookingForBlockState

	def gameTimeRemaining():
		return (self.startTime+(self.totalGameTime))-time.time() #returns time remaining in seconds

	def gameRunningTime():
		return time.time()-self.startTime

	def resetClock():
		self.startTime=time.time()
