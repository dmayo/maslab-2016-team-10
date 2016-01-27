from tamproxy.devices import Servo

class Arm:
	def __init__(self,tamp):
		self.tamp=tamp
		self.servo = Servo(self.tamp, 9)
		self.servo.bottom = 0
		self.servo.top = 200
		self.servo.speed = 30
		self.servo.write(self.servo.bottom)
		self.servoval = self.servo.bottom
		self.delta = 0