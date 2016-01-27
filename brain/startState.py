from state import state
class startState(state):
	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)
		print "start state"
	def run(self):

		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.updateGyro()
				self.sortBlock()
				
				if(not(self.finishedTurningNDegreesSlowly)):
					self.turnNDegreesSlowly(10)
					print "done turning"

				#print self.sensors.gyroCAngle
				#print self.actuators.sorter.sorterState
				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

		return startState(self.sensors, self.actuators)