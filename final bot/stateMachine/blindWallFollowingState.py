from state import state
import pickUpBlockState
import startState
import timeout

class BlindWallFollowingState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(BlindWallFollowingState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "starting blindWallFollowingState. This state performs 10 seconds of wall following without looking for blocks. It is meant to recover from not being able to move to a block."
		self.timeout = timeout.Timeout(5)

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				self.wallFollow("Right")

				#check timeout and block posession
				if self.timeout.isTimeUp() == True:
					print 'Done with blind wall following.'
					return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				if self.sensors.uIR.val == 0:
					print 'Break beam has sensed a block. Going to Pick Up Block State...'
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()