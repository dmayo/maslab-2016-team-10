from state import state
import turnToBlockState
import checkForMoreBlocksState
import pickUpBlockState
import math
import startState
import blindWallFollowingState

class MoveToBlockState(state):
	#substates: ApproachBlock, EatBlock, FlankManeuverTurn1, FlankManeuverTravel, FlankManeuverTurn2, DragBlock, PositionToDragBlock, Drag Block

	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(MoveToBlockState, self).__init__(sensors, actuators, motorController, timer, self.utils)
		
		self.CLOSE_ENOUGH_DISTANCE = 4 #make this such that the forward sensors will not detect a potential 90-degree corner while in approach mode
		self.ANGLE_EPSILON = 10
		self.DRIVE_SPEED = 40 #needs calibration
		self.EAT_DISTANCE = 7.1 #distance in inches we will drive forward to eat block
		self.ROBOT_RADIUS = 7.5
		self.CAMERA_OFFSET = 2.96
		self.start_gyro_angle = 0
		self.current_distance_traveled = 0

		self.FLANK_APPROACH_LENGHT = 2.5 #we hope the Flank Maneuver leaves us in a position straight in front of the block, 2.5 inches away
		self.FLANK_MANEUVER_MAX_ATTEMPTS = 3
		self.flank_first_angle = 0
		self.flank_target_distance = 0
		self.flank_isleftflank = False
		self.flank_maneuver_attempts = 0

		self.MIN_DRAG_BLOCK_DISTANCE = 1.1
		self.DRAG_TURN_RATE = 3
		self.DRAG_MAX_ATTEMPTS = 3
		self.drag_attempts = 0

		print "beginning MoveToBlockState"
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
					self.turnConstantRate(0)
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				#TODO: what if when the state starts, we are closer to the block than the CLOSE_ENOUGH_DISTANCE? That will cause changes needed in the EatBlock state collision code.
				if self.substate == "ApproachBlock":
					if self.sensors.camera.detectBlock == False:
						print 'Lost sight of block before we expected! Or did not find it after a flank maneuver. Falling back to startState...'
						return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					elif self.isColliding():
						self.motorController.fwdVel = 0
						isManueverPossible = self.calculateFlankManeuver()
						if isManueverPossible == True:
							self.turnNDegreesSlowly(self.flank_first_angle)
							self.flank_maneuver_attempts += 1
							self.substate = "FlankManeuverTurn1"
						else:
							print 'Area too cramped to start Flank Maneuver. Perhaps we are in a corner? Fall back to blind wall following...'
							return blindWallFollowingState.BlindWallFollowingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					elif self.sensors.camera.blockDistance < self.CLOSE_ENOUGH_DISTANCE:
						print 'Finished approaching block. Will now try to eat it.'
						self.substate = "EatBlock"
						self.motorController.fwdVel = self.DRIVE_SPEED
						self.sensors.encoders.resetEncoders()
					elif abs(self.sensors.camera.blockAngle) > self.ANGLE_EPSILON:
						print 'Have turned too far from the direction of the block. Will reposition...'
						self.motorController.fwdVel = 0
						return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif self.substate == "EatBlock":
					if self.isColliding():
						if self.current_distance_traveled >= self.MIN_DRAG_BLOCK_DISTANCE:
							if self.drag_attempts < self.DRAG_MAX_ATTEMPTS:
								self.drag_attempts += 1
								self.motorController.fwdVel = 0
								self.turnConstantRate(self.DRAG_TURN_RATE)
								self.substate = "DragBlock"
								self.start_gyro_angle = self.sensors.gyro.gyroCAngle
							else:
								Print 'After serveral drag attempts, it appears we are in a space too cramped to eat the block. Fall back to blind wall following...'
								return blindWallFollowingState.BlindWallFollowingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					elif self.current_distance_traveled >= self.EAT_DISTANCE:
						print 'Finished attempt to eat block. Break beam did not go off.'
						return checkForMoreBlocksState.CheckForMoreBlocksState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif self.substate == "DragBlock":
					if self.isColliding() == False:
						self.turnConstantRate(0)
						self.motorController.fwdVel = DRIVE_SPEED
						self.substate = "EatBlock"
					elif self.sensors.gyroCAngle >= (self.start_gyro_angle + 360):
						Print 'After a full 360, could not find a good position about which to turn. Being blind wall following...'
						self.turnConstantRate(0)
						return blindWallFollowingState.BlindWallFollowingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif self.substate == "FlankManeuverTurn1":
					if self.isFinishedTurning() == True:
						self.motorController.fwdVel = self.DRIVE_SPEED
						self.substate = "FlankManeuverTravel"
				elif self.substate == "FlankManeuverTravel":
					if self.isColliding():
						# keep turning until you find an opening or until you reach 90 degrees. If you reach 90 degrees, give up, you're cramped.
					elif self.current_distance_traveled >= self.flank_target_distance:
						self.motorController.fwdVel = 0
				elif self.substate == "FlankManeuverTurn2":
					if self.isFinishedTurning() == True:
						self.substate == "ApproachBlock"
				else:
					Print 'Error! Substate named ', self.substate, ' was not recognized. Exiting to Start State...'
					return startState.startState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	#collision detection avoids 1 inch of space on the sides. Trig was used to determine the lenght of the 30-degree angled sensors.
	#for the front sensors, we seek to avoid the worst case of a 90-degree angle, comes out to 2.9+.59 = about 3.5
	def isColliding(self):
		if self.sensors.irArray.ir_value[0] < 1 or self.sensors.irArray.ir_value[5] < 1:
			return True
		elif self.sensors.irArray.ir_value[1] < 2.32 or self.sensors.irArray.ir_value[4] < 2.32:
			return True
		elif self.sensors.irArray.ir_value[2] < 3.5 or self.sensors.irArray.ir_value[3] < 3.5:
			return True
		return False

	def isLeftClear(self):
		return (self.sensors.irArray.ir_value[0] < 1 and self.sensors.irArray.ir_value[1] < 2.32 and self.sensors.irArray.ir_value[2] < 3.5)

	def isRightClear(self):
		return (self.sensors.irArray.ir_value[5] < 1 and self.sensors.irArray.ir_value[4] < 2.32 and self.sensors.irArray.ir_value[3] < 3.5)


	#flank maneuver attempts to calculate parameters that will allow us to make a triangle motion to the cube such that our turn towards the cube will be 90 degrees
	#this is somewhat of a simple algorithm, a more complex one would use our sensor lenght differences to perform more complex geometry. We do not have the time to research or derive such things.
	#returns True if our surroundings will let us start the flank maneuver, false if not
	def calculateFlankManeuver(self):
		hyp = self.ROBOT_RADIUS + self.sensors.camera.blockDistance - self.CAMERA_OFFSET
		opp = self.ROBOT_RADIUS + self.FLANK_APPROACH_LENGHT
		angle = math.asin(opp/hyp)
		if isLeftClear() == True:
			self.flank_first_angle = angle
			self.flank_is_left = True
		elif isRightClear() == True:
			self.flank_first_angle = -angle
			self.flank_is_left = False
		else:
			return False
		self.flank_target_distance = math.sqrt(hyp**2-opp**2)
		self.flank_actual_distance = 0
		return True

