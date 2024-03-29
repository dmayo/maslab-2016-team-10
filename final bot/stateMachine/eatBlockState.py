from state import state
import turnToBlockState
import lookingForBlocksState
import pickUpBlockState
import math
import startState
import blindWallFollowingState
import timeout
import breakFreeState

class EatBlockState(state):
	#substates: ApproachBlock, EatBlock, FlankManeuverTurn1, FlankManeuverTravel, FlankManeuverTurn2, FlankManeuverReturn, DragBlock
	#flankManeuverStage: Turn1, Travel, Turn2, Return

	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(EatBlockState, self).__init__(sensors, actuators, motorController, timer, utils)

		print "EatBlockState"
		self.timeout = timeout.Timeout(30)

		self.DRIVE_SPEED = 60 #needs calibration
		self.eat_distance = 16 #distance in inches we will drive forward to eat block

		self.start_gyro_angle = 0

		self.DRAG_TURN_RATE = 30

		self.substate = "EatBlock"
		self.sensors.encoders.resetEncoders()
		

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				#State Timeout and break-beam detection
				if self.timeout.isTimeUp() == True:
					print 'State Timeout has timed out. Going to BreakFreeState...'
					return breakFreeState.BreakFreeState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				if self.sensors.uIR.val == 0:
					print 'Break beam has sensed a block. Going to Pick Up Block State...'
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				if self.substate == "EatBlock":
					self.driveStraight(self.DRIVE_SPEED)
					if self.isColliding():
						status_line = 'Collision Info: '
						for x in xrange(6):
							status_line +='Sensor '
							status_line += str(x)
							status_line += " :"
							status_line += "{:6.2f}".format(self.sensors.irArray.ir_value[x])
							status_line += " "
						print status_line
						self.driveStraight(0)
						self.eat_distance -= self.sensors.encoders.getDistanceTraveled()
						self.substate = "DragBlock"
					elif self.sensors.encoders.getDistanceTraveled() >= self.eat_distance:
						print 'Finished attempt to eat block. Break beam did not go off.'
						return lookingForBlocksState.LookingForBlocksState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif self.substate == "DragBlock":
					if self.isColliding() == False:
						print 'Found an opening we can move through.'
						self.turnConstantRate(0,"Right") #redundant?
						self.sensors.encoders.resetEncoders()
						self.substate = "EatBlock"
					elif self.sensors.gyro.gyroCAngle >= (self.start_gyro_angle + 360):
						print 'After a full 360, could not find a good position about which to turn. Begin blind wall following...'
						return blindWallFollowingState.BlindWallFollowingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					else:
						self.turnConstantRate(self.DRAG_TURN_RATE,"Right")
				else:
					print 'Error! Substate named ', self.substate, ' was not recognized. Exiting to Start State...'
					return startState.startState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()



