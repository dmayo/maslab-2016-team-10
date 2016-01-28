from tamproxy.devices import Motor
from sorter import Sorter
from arm import Arm

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
		self.arm = Arm(self.tamp)

		#sorting servo
		self.sorter = Sorter(self.tamp)

	def update(self):
		self.arm.update()
		self.sorter.update()
