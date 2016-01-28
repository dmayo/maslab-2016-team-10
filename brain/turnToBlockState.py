from state import state

class TurnToBlockState(state):

	epsilon = 3
	turn_attempts = 0
	max_turn_attempts = 5

	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)
		print "beginning Turn to block state"
	def run(self):

		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.updateGyro()

				if self.camera.detectBlock == False:
					print "Lost sight of block while turning!"
					return wallFollowingState(self.sensors,self.actuators,self.motorController,self.timer) #TODO: get actual state name
				else if self.finishedTurningNDegreesSlowly == True:
				print "Robot stationary. Pointing towards target?"
				if self.camera.blockAngle <= epsilon:
					print "Yes!"
					return attackBlockState(self.sensors,self.actuators,self.motorController,self.timer)
				else:
					print "No. Off by ", self.camera.blockAngle, ". Have made ", turn_attempts, " turn attempt(s)."
					turn_attempts += 1
					if turn_attempts < max_turn_attempts:
						self.turnNDegreesSlowly(self.sensors.camera.blockAngle)
					else:
						print "Giving up. Turning failed!" #TODO: this should hopefully never happen. If it does, it means our PID needs tuning!
						return breakFreeState(self.sensors,self.actuators,self.motorController,self.timer)

						#while robot is seeing block and turning, code does nothing, just lets robot turn

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

			return startState(self.sensors, self.actuators)
