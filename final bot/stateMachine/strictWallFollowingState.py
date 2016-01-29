from state import state
import turnToBlockState
import lookingForBlocksState
import pickUpBlockState
import time
import randomTravelingState
import timeout
import startState

#if it sees a block -> turnToBlockState
#else -> wall follow
#if no block found after a little while -> lookingForBlocksState

class StrictWallFollowingState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(StrictWallFollowingState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Strict Wall Following State starting. In this state, we don't chase a block unless we are close to it..."
		self.timeout = timeout.Timeout(10) #attempt to get closer for 10 seconds
		self.STRICT_BLOCK_DISTANCE_THRESHOLD = 8 #distance at which we start chasing block

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				#check timeout and block posession
				if self.timeout.isTimeUp() == True:
					print 'StrictWallFollowingState complete. Did not find the block again...'
					return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				if self.sensors.uIR == 0:
					print 'Break beam has sensed a block. Going to Pick Up Block State...'
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.wallFollow("Right")

				if self.sensors.camera.detectBlock and self.sensors.camera.blockDistance < self.STRICT_BLOCK_DISTANCE_THRESHOLD:
					return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				
				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()