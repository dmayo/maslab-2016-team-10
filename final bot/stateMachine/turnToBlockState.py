from state import state
import wallFollowingState
import lookingForBlocksState
import moveToBlockState
import breakFreeState
import timeout

#if it doesn't see a block -> lookForBlockState
#if the block is centered in the camera view -> moveToBlock
#else -> turn to center block in the camera view

class TurnToBlockState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(TurnToBlockState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Turn to block state"
		self.BLOCK_ANGLE_EPSILON = 1
		self.timeout = timeout.Timeout(10)

	def run(self):

		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				#State Timeout and break-beam detection
				if self.timeout.isTimeUp() == True:
					print 'State Timeout has timed out. Going to BreakFreeState...'
					return breakFreeState.BreakFreeState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				if self.sensors.uIR == 0:
					print 'Break beam has sensed a block. Going to Pick Up Block State...'
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				if self.sensors.camera.detectBlock == False:
					print "Lost sight of block while turning!"
					return lookingForBlocksState.LookingForBlocksState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)
				elif self.isFinishedTurning():
					print "ready to move to block"
					print self.sensors.camera.blockAngle
					return moveToBlockState.MoveToBlockState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)
				else:
					print "turning to block"
					self.turnNDegreesSlowly(self.sensors.camera.blockAngle)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()
