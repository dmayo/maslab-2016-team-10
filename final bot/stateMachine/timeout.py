import time

class Timeout(object):

	def __init__(self, length):
		self.timeout_length = length
		self.reset()

	def reset(self):
		self.startTime = time.time()
		self.isExpired = False

	def isTimeUp():
		return ((time.time() - self.startTime) >= self.timeout_length)

	def setExpired():
		self.isExpired = True


