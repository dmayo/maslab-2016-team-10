from state import state
import wallFollowingState
import moveToBlockState

#if it doesn't see a block -> lookForBlockState
#if the block is centered in the camera view -> moveToBlock
#else -> turn to center block in the camera view

class TurnToBlockState(state):
	
	turn_attempts = 0
	max_turn_attempts = 5

	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)
		print "beginning Turn to block state"
		self.BLOCK_ANGLE_EPSILON = 3
	def run(self):

		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				if self.camera.detectBlock == False:
					print "Lost sight of block while turning!"
					return lookingForBlockState(self.sensors,self.actuators,self.motorController,self.timer)
				elif self.camera.blockAngle <= self.BLOCK_ANGLE_EPSILON:
					print "Yes!"
					#return AttackBlockState(self.sensors,self.actuators,self.motorController,self.timer)
				else:
					self.turnNDegreesSlowly(self.sensors.camera.blockAngle)
					'''
					print "No. Off by ", self.camera.blockAngle, ". Have made ", turn_attempts, " turn attempt(s)."
					turn_attempts += 1
					if turn_attempts < max_turn_attempts:
						self.turnNDegreesSlowly(self.sensors.camera.blockAngle)
					else:
						print "Giving up. Turning failed!" #TODO: this should hopefully never happen. If it does, it means our PID needs tuning!
						return BreakFreeState(self.sensors,self.actuators,self.motorController,self.timer)

						#while robot is seeing block and turning, code does nothing, just lets robot turn
					'''
				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()
