from state import state
from turnToBlockState import *
from checkForMoreBlocksStates import *


#if it sees a block -> turnToBlockState
#else -> scan for blocks
#if finish scan and no blocks found -> wall follow

class LookingForBlocksState(state):
	def __init__(self, sensors, actuators, motorController, timer):
		super(LookingForBlocksState, self).__init__(sensors, actuators, motorController, timer)
		print "Looking For Blocks State"
		self.SCAN_SPEED=3
		self.initialAngle=self.sensors.gyro.gyroCAngle

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				if self.sensors.camera.detectBlock:
					return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer)
				elif self.sensors.gyro.gyroCAngle>self.initialAngle+360:
					return wallFollowingState.WallFollowingState(self.sensors, self.actuators, self.motorController, self.timer)
				else:
					self.turnConstantRate(self.SCAN_SPEED)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()