from state import state
import wallFollowingState
import lookingForBlocksState
import moveToBlockState

#if it doesn't see a block -> lookForBlockState
#if the block is centered in the camera view -> moveToBlock
#else -> turn to center block in the camera view

class TurnToBlockState(state):
	def __init__(self, sensors, actuators, motorController, timer):
		super(TurnToBlockState, self).__init__(sensors, actuators, motorController, timer)
		print "Turn to block state"
		self.BLOCK_ANGLE_EPSILON = 1
	def run(self):

		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				if self.sensors.camera.detectBlock == False:
					print "Lost sight of block while turning!"
					return lookingForBlocksState.LookingForBlocksState(self.sensors,self.actuators,self.motorController,self.timer)
				elif abs(self.sensors.camera.blockAngle) <= self.BLOCK_ANGLE_EPSILON:
					print "ready to move to block"
					print self.sensors.camera.blockAngle
					return moveToBlockState.MoveToBlockState(self.sensors,self.actuators,self.motorController,self.timer)
				else:
					self.turnNDegreesSlowly(self.sensors.camera.blockAngle)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()
