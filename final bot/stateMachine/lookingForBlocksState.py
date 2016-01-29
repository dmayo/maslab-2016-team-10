from state import state
import turnToBlockState
import checkForMoreBlocksState
import wallFollowingState
import randomTravelingState
import pickUpBlockState
import timeout


#if it sees a block -> turnToBlockState
#else -> scan for blocks
#if finish scan and no blocks found -> wall follow

class LookingForBlocksState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(LookingForBlocksState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Looking For Blocks State"
		self.SCAN_SPEED=30
		self.initialAngle=self.sensors.gyro.gyroCAngle
		self.timeout = timeout.Timeout(20)

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				if self.timeout.isTimeUp() == True:
					print 'State Timeout has timed out. Going to Random Travel State...'
					return randomTravelingState.RandomTravelingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				if self.sensors.uIR.val == 0:
					print 'Break beam has sensed a block. Going to Pick Up Block State...'
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				if self.sensors.camera.detectBlock:
					print "Found Block"
					return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif self.sensors.gyro.gyroCAngle>self.initialAngle+360:
					return wallFollowingState.WallFollowingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				else:
					self.turnConstantRate(self.SCAN_SPEED,"Right")

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()