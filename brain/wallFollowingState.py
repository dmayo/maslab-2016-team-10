from state import state
from turnToBlockState import TurnToBlockState
from lookingForBlocksState import LookingForBlocksState
import time

#if it sees a block -> turnToBlockState
#else -> wall follow
#if no block found after a little while -> lookingForBlocksState

class wallFollowingState(state):
	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)
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
				
				self.wallFollow("Left")

				if self.sensors.camera.detectBlock:
					return TurnToBlockState(slef.sensors, slef.actuators, slef.motorController, slef.timer)
				elif (time.time()-self.startStateTime)>=self.WALL_FOLLOW_TIME:
					return LookingForBlocksState(slef.sensors, slef.actuators, slef.motorController, slef.timer)
				else:
					self.turnConstantRate(self.SCAN_SPEED)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()