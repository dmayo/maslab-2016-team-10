from state import state
import wallFollowingState
import turnToBlockState
import lookingForBlocksState
import time

#if it sees a block -> get block
#else -> scan for blocks

class startState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(startState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Start State"
		self.START_GAME_DELAY=3 #in seconds

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()
				
				if self.sensors.button.val==1 and self.utils.isGameStarted==False:
					self.utils.isGameStarted=True
					self.utils.startTime=time.time()

				if(self.utils.isGameStarted==True and time.time()-self.utils.startTime>self.START_GAME_DELAY):
					if self.sensors.camera.detectBlock:
						return turnToBlockState.TurnToBlockState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)
					else:
						self.utils.navTimeout.reset()
						return lookingForBlocksState.LookingForBlocksState(self.sensors,self.actuators,self.motorController,self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()