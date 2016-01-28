from state import state
import turnToBlockState
import checkForMoreBlocksState
import pickUpBlockState

class MoveToBlockState(state):
	#substates: ApproachBlock, EatBlock

	def __init__(self, sensors, actuators, motorController, timer):
		super(MoveToBlockState, self).__init__(sensors, actuators, motorController, timer)
		print "beginning MoveToBlockState"
		self.CLOSE_ENOUGH_DISTANCE = 3
		self.ANGLE_EPSILON = 10
		self.DRIVE_SPEED = 40 #needs calibration
		self.EAT_DISTANCE = 9 #distance in inches we will drive forward to eat block
		self.substate = "ApproachBlock"
		self.motorController.fwdVel = self.DRIVE_SPEED

	def run(self):

		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				#constantly check to see if we have something to eat
				if self.sensors.uIR == 0:
					self.motorController.fwdVel = 0
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer)

				if self.substate == "ApproachBlock":
					#TODO: Assuming here we always see block. Maybe put in what happens if we lose sight of the block? (why would that happen? If Erin removes it.)
					if self.sensors.camera.blockDistance < self.CLOSE_ENOUGH_DISTANCE:
						print 'Finished approaching block. Will now try to eat it.'
						self.substate = "EatBlock"
						self.motorController.fwdVel = 0
						self.dummyDriveDistance(self.EAT_DISTANCE)
					elif abs(self.sensors.camera.blockAngle) > self.ANGLE_EPSILON:
						print 'Have turned too far from the direction of the block. Will reposition...'
						self.motorController.fwdVel = 0
						return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer)
				elif self.substate == "EatBlock":
					if self.dummyHasFinishedDrivingDistance() == True:
						print 'Finished attempt to eat block. Break beam did not go off.'
						return checkForMoreBlocksState.CheckForMoreBlocksState(self.sensors, self.actuators, self.motorController, self.timer)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	def dummyDriveDistance(self,distance):
		pass

	def dummyHasFinishedDrivingDistance(self):
		return True
