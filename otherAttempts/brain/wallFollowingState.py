from state import state
import turnToBlockState
import lookingForBlocksState
import time

#if it sees a block -> turnToBlockState
#else -> wall follow
#if no block found after a little while -> lookingForBlocksState

class WallFollowingState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(WallFollowingState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Wall Following State"
		self.SCAN_SPEED=3
		self.initialAngle=self.sensors.gyro.gyroCAngle
		self.startStateTime=time.time()
		self.WALL_FOLLOW_TIME=10 #time before looking around in seconds

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				self.wallFollow("Right")

				if self.sensors.camera.detectBlock:
					return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif (time.time()-self.startStateTime)>=self.WALL_FOLLOW_TIME:
					return lookingForBlocksState.LookingForBlocksState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				else:
					self.turnConstantRate(self.SCAN_SPEED)
				
				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()