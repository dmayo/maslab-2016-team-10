from state import state
import wallFollowingState
import turnToBlockState
import lookingForBlocksState
import time
import testState
import randomTravelingState
import breakFreeState

#if it sees a block -> get block
#else -> scan for blocks

class startState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(startState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Start State"
		self.START_GAME_DELAY=0 #in seconds
		self.turnNDegreesSlowly(0)
		self.motorController.updateMotorSpeeds()

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				if self.sensors.button.val==1 and self.utils.isGameStarted==False:
					self.utils.isGameStarted=True
					self.utils.startTime=time.time()

				if(self.utils.isGameStarted==True and time.time()-self.utils.startTime>self.START_GAME_DELAY):
					#return testState.TestState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)
					'''
					if self.sensors.camera.detectBlock:
						return turnToBlockState.TurnToBlockState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)
					else:
						self.utils.navTimeout.reset()
						return lookingForBlocksState.LookingForBlocksState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)
					'''
					#return randomTravelingState.RandomTravelingState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)
					#return breakFreeState.BreakFreeState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)
					return wallFollowingState.WallFollowingState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()