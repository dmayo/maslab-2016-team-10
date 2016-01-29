from state import state
import wallFollowingState
import turnToBlockState
import lookingForBlocksState
import time
import startState

class BreakFreeState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(BreakFreeState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Break Free State..."

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				print 'Break Free State not implemented. Going back to Start state...'
				return startState.startState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()