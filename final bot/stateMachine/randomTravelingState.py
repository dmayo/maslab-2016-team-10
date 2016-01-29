from state import state
import wallFollowingState
import turnToBlockState
import lookingForBlocksState
import time
import timeout
import startState

#substates: RandomTraveling, Turning, Scanning

class RandomtTravelingState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		print "Starting RandomtTravelingState..."
		self.timeout = timeout.Timeout(30)
		self.substate = "RandomTraveling"

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				if self.timeout.isTimeUp() == True:
					print 'State Timeout has timed out. Going to StartState...'
					return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				if self.sensors.uIR == 0:
					print 'Break beam has sensed a block. Going to Pick Up Block State...'
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
			
				if self.substate == "RandomTraveling":
					pass
				elif self.substate == "Turning":
					pass
				elif self.substate == "Scanning":
					pass
				else:
					print 'Error! Substate ', self.substate, ' not a valid substate. Returning to StartState...'
					return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()