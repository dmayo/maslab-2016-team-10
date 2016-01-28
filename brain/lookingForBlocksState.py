from state import state
from turnToBlockState import TurnToBlockState

#if it sees a block -> turnToBlockState
#else -> scan for blocks
#if finish scan and no blocks found -> wall follow

class LookingForBlocksState(state):
	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)
		print "Looking For Blocks State"
		self.SCAN_SPEED=3

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				if self.sensors.camera.detectBlock:
					return TurnToBlockState(slef.sensors, slef.actuators, slef.motorController, slef.timer)
				else:
					turnConstantRate(self.SCAN_SPEED)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()