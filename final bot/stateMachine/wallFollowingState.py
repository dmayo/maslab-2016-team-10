from state import state
import turnToBlockState
import lookingForBlocksState
import time
import randomTravelingState
import timeout

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

				#check timeout and block posession
				if self.utils.navTimeout.isTimeUp() == True:
					print 'Navigation Timeout timed out. Going to Random Traveling State...'
					return randomTravelingState.RandomTravelingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				if self.sensors.uIR == 0:
					print 'Break beam has sensed a block. Going to Pick Up Block State...'
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.wallFollow("Right")

				if self.sensors.camera.detectBlock:
					return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif (time.time()-self.startStateTime)>=self.WALL_FOLLOW_TIME:
					return lookingForBlocksState.LookingForBlocksState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				
				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()