from state import state
import wallFollowingState
import startState

#TODO: this is a stub state. It should be identical

class blindWallFollowingState(state):
	def __init__(self, sensors, actuators, motorController, timer):
		super(blindWallFollowingState, self).__init__(sensors, actuators, motorController, timer)
		print "starting blindWallFollowingState"

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				#stub: replace with actual code
				return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()