from state import state

#if it sees a block -> get block
#else -> scan for blocks

class startState(state):
	time_blocks = 0
	stop_time = 50 #5 seconds

	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)
		print "start state"

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				if time_blocks == 0:
					self.motorController.desiredAngle = self.sensors.gyro.gyroCAngle
					self.fwdVel = 40

				time_blocks += 1

				if time_blocks >= stoptime:
					self.fwdVel = 0

				print 'At', str(time_blocks * .1), ' sec, Left Encoder value: ', self.sensors.encoderL.val

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

		return startState(slef.sensors, slef.actuators, slef.motorController, slef.timer)
