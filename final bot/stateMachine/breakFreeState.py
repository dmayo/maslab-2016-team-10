from state import state
import wallFollowingState
import turnToBlockState
import lookingForBlocksState
import time
import startState
import random
import timeout

class BreakFreeState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(BreakFreeState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Break Free State. Starting by backing up..."
		random.seed(time.time())
		self.backUpTimeout = timeout.Timeout(random.randrange(3,6))
		self.stateTimeout = timeout.Timeout(10)
		self.substate = "backUp"
		self.BACK_UP_SPEED = -40

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				if self.stateTimeout.isTimeUp() == True or self.isClearOfSurroundings():
					print 'Breaking Free is finished. Returning to startState...'
					return startState.startState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				
				if self.substate == "backUp":
					if self.backUpTimeout.isTimeUp():
						print 'Done backing up. Now turning...'
						self.substate = "Turning"
						if self.isLeftFree():
							self.turnNDegreesSlowly(random.randrange(60,120))
						else:
							self.turnNDegreesSlowly(random.randrange(-120,-60))
					else:
						self.driveStraight(self.BACK_UP_SPEED)
				if self.substate == "Turning":
					if self.isFinishedTurning():
						return startState.startState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	def isLeftFree(self):
		if self.checkIndividualSensor(0,1):
			return False
		if self.checkIndividualSensor(1,2.3):
			return False
		return True

	def isRightFree(self):
		if self.checkIndividualSensor(5,1):
			return False
		if self.checkIndividualSensor(4,2.3):
			return False
		return True

	def isClearOfSurroundings(self):
		if self.checkIndividualSensor(0,3):
			return False
		if self.checkIndividualSensor(1,5):
			return False
		if self.checkIndividualSensor(2,9):
			return False
		if self.checkIndividualSensor(3,9):
			return False
		if self.checkIndividualSensor(4,5):
			return False
		if self.checkIndividualSensor(5,3):
			return False
		return True




