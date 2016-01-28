from state import state
import startState

class CheckForMoreBlocksState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(CheckForMoreBlocksState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "starting CheckForMoreBlocksState"

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				#stubState
				return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()