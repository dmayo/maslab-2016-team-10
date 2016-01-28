from state import state
from turnToBlockState import TurnToBlockState
from lookingForBlocksState import LookingForBlocksState

#if it sees a block -> get block
#else -> scan for blocks

class startState(state):
	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				if self.sensors.camera.detectBlock:
					return TurnToBlockState(slef.sensors, slef.actuators, slef.motorController, slef.timer)
				else:
					return LookingForBlocksState(slef.sensors, slef.actuators, slef.motorController, slef.timer)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()
