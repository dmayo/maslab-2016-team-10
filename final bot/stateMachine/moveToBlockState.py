from state import state
import turnToBlockState
import checkForMoreBlocksState
import pickUpBlockState
import math
import startState
import blindWallFollowingState
import timeout
import eatBlockState
import breakFreeState

class MoveToBlockState(state):
	#substates: ApproachBlock, EatBlock, FlankManeuverTurn1, FlankManeuverTravel, FlankManeuverTurn2, FlankManeuverReturn, DragBlock
	#flankManeuverStage: Turn1, Travel, Turn2, Return

	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(MoveToBlockState, self).__init__(sensors, actuators, motorController, timer, utils)

		print "MoveToBlockState"
		self.timeout = timeout.Timeout(30)
		
		self.CLOSE_ENOUGH_DISTANCE = 4 #make this such that the forward sensors will not detect a potential 90-degree corner while in approach mode
		self.ANGLE_EPSILON = 10

		self.DRIVE_SPEED = 60 #needs calibration
		self.EAT_DISTANCE = 7.1 #distance in inches we will drive forward to eat block

		self.ROBOT_RADIUS = 7.5
		self.CAMERA_OFFSET = 2.96
		self.start_gyro_angle = 0

		self.MIN_DISTANCE_TO_START_FLANK_MANEUVER = 12 #don't even try the flank if we are further than 15 inches away
		self.FLANK_APPROACH_LENGHT = 2.5 #we hope the Flank Maneuver leaves us in a position straight in front of the block, 2.5 inches away
		self.FLANK_MANEUVER_MAX_ATTEMPTS = 3
		self.flank_first_angle = 0
		self.flank_second_angle = 0
		self.flank_target_distance = 0
		self.flank_is_left = False
		self.flank_maneuver_attempts = 0
		self.flank_initial_distance_from_block = 0

		self.MIN_DRAG_BLOCK_DISTANCE = 1.1
		self.DRAG_TURN_RATE = 3
		self.DRAG_MAX_ATTEMPTS = 3
		self.drag_attempts = 0

		self.substate = "ApproachBlock"
		self.FlankManeuverStage = "Turn1"
		

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

				#TODO: what if when the state starts, we are closer to the block than the CLOSE_ENOUGH_DISTANCE? That will cause changes needed in the EatBlock state collision code.
				#TODO: (minor) there is code duplication between collision code sections of ApproachBlock and EatBlock code
				if self.substate == "ApproachBlock":
					print 'Starting Approach...'
					#self.driveStraight(self.DRIVE_SPEED)
					self.turnNDegreesAndMove(self.sensors.camera.blockAngle,self.DRIVE_SPEED)
					if self.sensors.camera.detectBlock == False:
						print 'Cannot see block anymore. May be too close. Will try to eat it.'
						return eatBlockState.EatBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					elif self.isColliding():
						canOvercomeCollision = self.dealWithCollision() #dealWithCollision will take care of changing the substate
						if canOvercomeCollision == False:
							print 'Area too cramped to overcome collision. Perhaps we are in a corner? Fall back to strict wall following...'
							return blindWallFollowingState.BlindWallFollowingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif self.substate == "FlankManeuver":
					self.performFlankManeuver()
				elif self.substate == "FlankFailed":
					print 'Flank Failed. Going to blind wall follow'
					return blindWallFollowingState.BlindWallFollowingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				else:
					print 'Error! Substate named ', self.substate, ' was not recognized. Exiting to Start State...'
					return startState.startState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	def isLeftClear(self):
		return (self.sensors.irArray.ir_value[0] < 1 and self.sensors.irArray.ir_value[1] < 2.32)

	def isRightClear(self):
		return (self.sensors.irArray.ir_value[5] < 1 and self.sensors.irArray.ir_value[4] < 2.32)

	def dealWithCollision(self):
		status_line = 'Collision Info: '
		for x in xrange(6):
			status_line +='Sensor '
			status_line += str(x)
			status_line += " :"
			status_line += "{:6.2f}".format(self.sensors.irArray.ir_value[x])
			status_line += " "
		print status_line
		print 'Too close to a wall. Can attempt flank maneuver?'
		isManueverPossible = self.calculateFlankManeuver(self.sensors.camera.blockDistance)
		if isManueverPossible == True:
			print 'Yes. Starting flank maneuver with angle ', self.flank_first_angle
			self.turnNDegreesSlowly(self.flank_first_angle)
			self.flank_maneuver_attempts += 1
			self.eat_distance -= self.sensors.encoders.getDistanceTraveled()
			self.sensors.encoders.resetEncoders()
			self.substate = "FlankManeuver"
			return True
		else:
			return False

	#flank maneuver attempts to calculate parameters that will allow us to make a triangle motion to the cube such that our turn towards the cube will be 90 degrees
	#this is somewhat of a simple algorithm, a more complex one would use our sensor lenght differences to perform more complex geometry. We do not have the time to research or derive such things.
	#returns True if our surroundings will let us start the flank maneuver, false if not
	def calculateFlankManeuver(self,distanceFromBlock):
		dist_to_block = self.ROBOT_RADIUS + distanceFromBlock - self.CAMERA_OFFSET
		approach_dist = self.ROBOT_RADIUS + self.FLANK_APPROACH_LENGHT

		if dist_to_block < 0:
			return False

		self.flank_initial_distance_from_block = dist_to_block

		abs_first_angle = 90
		abs_second_angle = 90
		if approach_dist > dist_to_block:
			abs_second_angle = 180-math.degrees(math.asin(dist_to_block/approach_dist))
			self.flank_target_distance = math.sqrt(approach_dist**2-dist_to_block**2)
		elif dist_to_block > approach_dist:
			abs_first_angle = math.degrees(math.asin(approach_dist/dist_to_block))
			self.flank_target_distance = math.sqrt(dist_to_block**2-approach_dist**2)
		else:
			#special case: both sides same, make equilateral triangle
			if self.isLeftClear() == True:
				self.flank_first_angle = 60
				self.flank_second_angle = -120
				self.flank_target_distance = approach_dist
				self.flank_is_left = True
				return True
			elif self.isRightClear() == True:
				self.flank_first_angle = -60
				self.flank_second_angle = 120
				self.flank_target_distance = approach_dist
				self.flank_is_left = False
				return True
			else:
				return False

		if self.isLeftClear() == True:
			self.flank_first_angle = abs_first_angle
			self.flank_second_angle = -abs_second_angle
			self.flank_is_left = True
		elif self.isRightClear() == True:
			self.flank_first_angle = -abs_first_angle
			self.flank_second_angle = abs_second_angle
			self.flank_is_left = False
		else:
			return False

		return True

	#if we collide during the travel phase of the Flank Maneuver, this calculates the angle we need to turn to point the robot back at the block
	#the calculateRecoveryAngle function needs work! Does not currently work! Will leave for later when less urgent stuff is taken care of.
	"""def calculateRecoveryAngle(self):
		#We want to calculate a recovery angle that forms part of a triangle (not necessarily a right triangle).
		#We know two sides: the side we traveled "b", and the side that represented how far we were from the block to being with "a"
		#We know the angle we turned, "C"
		side_b = self.sensors.encoders.getDistanceTraveled()
		side_a = self.flank_initial_distance_from_block
		angle_radians_C = math.radians(self.flank_first_angle)

		#Let's use the law of cosines to caculate the third side of the triangle "c"
		side_c = math.sqrt(side_a**2 + side_b**2 -2*side_a*side_b*math.cos(angle_radians_C))

		#Now let's use law of sines to get the angle we want to turn,
		angle_A = math.degrees(math.asin(side_a*math.sin(angle_radians_C)/side_c))

		if self.flank_is_left:
			return 180-(-angle_A)
		else:
			return 180-angle_A"""

	def performFlankManeuver(self):
		if self.FlankManeuverStage == "Turn1":
			if self.isFinishedTurning() == True:
				print 'Finished first Flank Maneuver turn. Now going straight'
				self.driveStraight(self.DRIVE_SPEED)
				self.FlankManeuverStage = "Travel"
		elif self.FlankManeuverStage == "Travel":
			if self.isColliding():
				print 'No room while in Flank Maneuver travel. Reporting Failure...'
				self.driveStraight(0)
				#self.turnNDegreesSlowly(self.calculateRecoveryAngle())
				self.substate = "FlankFailed"
			elif self.sensors.encoders.resetEncoders() >= self.flank_target_distance:
				print 'Finished flank maneuver travel. Performing second turn...'
				self.driveStraight(0)
				self.turnNDegreesSlowly(self.flank_second_angle)
				self.FlankManeuverStage = "Turn2"
		elif self.FlankManeuverStage == "Turn2":
			if self.isFinishedTurning() == True:
				print 'Flank Maneuver complete. Should now be pointing at block from better angle.'
				self.sensors.encoders.resetEncoders()
				self.substate == "ApproachBlock"
		elif self.FlankManeuverStage == "Return":
			if self.isFinishedTurning() == True:
				print 'Recovery complete. Returning to ApproachBlock substate...'
				self.substate = "ApproachBlock"
		else:
			print 'Bad Flank Maeuver Stage name: ', self.flankManeuverStage, '. Exiting to ApproachBlock substate...'
			self.substate = "ApproachBlock"



