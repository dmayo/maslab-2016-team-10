from state import state
import wallFollowingState
import turnToBlockState
import lookingForBlocksState
import time

#if it sees a block -> get block
#else -> scan for blocks

class TestState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(TestState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "In Test State..."
		self.driveStraight(0)

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				for x in xrange(6):
    				print 'Sensor ', x, " :" ,"{:6.2f}".format(self.sensors.irArray.ir_value[x])

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()