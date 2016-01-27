from pipeReader import PipeReader

class Camera:
	def __init__(self):
		self.cameraPipe = PipeReader('./image')
		self.detectBlock = False
		self.blockDistance = 0
		self.blockAngle = 0

	def update(self):
		#message = self.cameraPipe.read(20)
		message=""
		if message:
			print("Recieved: '%s'" % message)
			if message[:2] == 'no':
				self.detectBlock=False
			else:
				try:
					self.detectBlock=True
					self.blockDistance, self.blockAngle = [number[:6] for number in message.split(',')]
				except:
					print "garbage message"