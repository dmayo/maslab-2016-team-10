from state import state

class AttackBlockState(state):

	close_enough_distance = 3 #distance in inches at which we are close enough to try eating the block

	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)
		print "beginning AttackBlockState"

	def run(self):

		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

                      
				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

		return startState(slef.sensors, slef.actuators, slef.motorController, slef.timer)
