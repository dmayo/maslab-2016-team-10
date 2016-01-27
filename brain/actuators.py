from tamproxy.devices import Motor
from tamproxy.devices import Servo
from sorter import Sorter

class Actuators:
	def __init__(self,tamp):
		self.tamp=tamp
				
		#motor left
		self.motorL = Motor(self.tamp, 2, 4)
		self.motorL.write(1,0)

		#motor right
		self.motorR = Motor(self.tamp,1, 3)
		self.motorR.write(1,0)

		#arm servo
		self.servo = Servo(self.tamp, 9)
		self.servo.bottom = 0
		self.servo.top = 200
		self.servo.speed = 30
		self.servo.write(self.servo.bottom)
		self.servoval = self.servo.bottom
		self.delta = 0

		#sorting servo
		self.sorter = Sorter(self.tamp)

	def update(self):
		self.sorter.update()
