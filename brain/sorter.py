from tamproxy.devices import Servo

class Sorter:
	def __init__(self, tamp):
		self.tamp=tamp
		self.servo = Servo(self.tamp, 5)
		self.servo.center = 90
		self.servo.right = 25
		self.servo.left = 165
		self.servo.speed = 15

		self.servo.write(self.servo.center)
		self.sorterval = self.servo.center
		self.dsorter = 0
		self.sorterState = "None"

	def moveSorterLeft(self):
		print "moving left"
		if self.sorterval < self.servo.left:
			self.sorterState="Left"
			self.dsorter = self.servo.speed
		elif self.sorterval >= self.servo.left:
			self.sorterState="Center"
			self.dsorter = 0

	def moveSorterRight(self):
		if self.sorterval > self.servo.right:
			self.sorterState="Right"
			self.dsorter = -self.servo.speed
		elif self.sorterval <= self.servo.right:
			self.sorterState="Center"
			self.dsorter = 0

	def moveSorterCenter(self):
		self.sorterState="None"
		self.sorterval = self.servo.center

	def update(self):
		if(self.sorterState!="None"):
			if(self.sorterState=="Left"):
				self.moveSorterLeft()
			elif(self.sorterState=="Reft"):
				self.moveSorterRight()
			elif(self.sorterState=="Center"):
				self.moveSorterCenter()
			self.sorterval += self.dsorter
	        self.servo.write(abs(self.sorterval))
