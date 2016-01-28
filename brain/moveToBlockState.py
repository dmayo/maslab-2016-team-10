from state import state
import turnToBlockState
import checkForMoreBlocksState
import pickUpBlockState
import math
import startState
import blindWallFollowingState

class MoveToBlockState(state):
	#substates: ApproachBlock, EatBlock, FlankManeuverTurn1, FlankManeuverTravel, FlankManeuverTurn2, DragBlock, PositionToDragBlock, Drag Block

	def __init__(self, sensors, actuators, motorController, timer):
		super(MoveToBlockState, self).__init__(sensors, actuators, motorController, timer)
		print "beginning MoveToBlockState"
		self.CLOSE_ENOUGH_DISTANCE = 4 #make this such that the forward sensors will not detect a potential 90-degree corner while in approach mode
		self.ANGLE_EPSILON = 10
		self.DRIVE_SPEED = 40 #needs calibration
		self.EAT_DISTANCE = 9 #distance in inches we will drive forward to eat block
		self.SAFE_DISTANCE = 1.5 #distance at which we want to stop travelling to avoid a collision
		self.substate = "ApproachBlock"
		self.motorController.fwdVel = self.DRIVE_SPEED
		self.FLANK_APPROACH_LENGHT = 2.5 #we hope the Flank Maneuver leaves us in a position straight in front of the block, 2.5 inches away
		self.ROBOT_RADIUS = 7.5 #radius of the robot
		self.CAMERA_OFFSET = 2.96
		self.flank_first_angle = 0
		self.flank_target_distance = 0
		self.flank_actual_distance = 0

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
					if self.isColliding():
						isManueverPossible = self.calculateFlankManeuver()
						if isManueverPossible == True:
							self.turnNDegreesSlowly(self.flank_first_angle)
							self.substate = "FlankManeuverTurn1"
						else:
							print 'Area too cramped to start Flank Maneuver. Perhaps we are in a corner? Being blind wall following.'
							return blindWallFollowingState.BlindWallFollowingState(self.sensors, self.actuators, self.motorController, self.timer)
						elif self.sensors.camera.blockDistance < self.CLOSE_ENOUGH_DISTANCE:
						print 'Finished approaching block. Will now try to eat it.'
						self.substate = "EatBlock"
						self.motorController.fwdVel = 0
						self.dummyDriveDistance(self.EAT_DISTANCE)
					elif abs(self.sensors.camera.blockAngle) > self.ANGLE_EPSILON:
						print 'Have turned too far from the direction of the block. Will reposition...'
						self.motorController.fwdVel = 0
						return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer)
				elif self.substate == "EatBlock":
					if self.isColliding():
						#To implement: if we got close enough, go to drag block state until we are free to move again.
						#Otherwise, see if you can't scan the area to make sure you're gonna crash if you keep going forward
						#if you do find you will crash, see if you can do a tight flank maneuver, or just give up
						#FORGET IT, don't do scan. Go straight to drag or flank maneuver.
					elif self.dummyHasFinishedDrivingDistance() == True:
						print 'Finished attempt to eat block. Break beam did not go off.'
						return checkForMoreBlocksState.CheckForMoreBlocksState(self.sensors, self.actuators, self.motorController, self.timer)
				elif self.substate == "FlankManeuverTurn1":
					if self.dummyHasTurnFinished() == True:
						self.motorController.fwdVel = self.DRIVE_SPEED
						self.substate = "FlankManeuver2"
				elif self.substate == "FlankManeuverTravel":
					if self.isColliding():
						# keep turning until you find an opening or until you reach 90 degrees. If you reach 90 degrees, give up, you're cramped.
					else
					#TODO:					


				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()


	def dummyHasFinishedDrivingDistance(self):
		return True

	def dummyHasTurnFinished(self):
		return True

	#collision detection avoids 1 inch of space on the sides. Trig was used to determine the lenght of the 30-degree angled sensors.
	#for the front sensors, we seek to avoid the worst case of a 90-degree angle, comes out to 2.9+.59 = about 3.5
	def isColliding(self):
		if self.sensors.irArray.ir_value[0] < 1 or self.sensors.irArray.ir_value[5] < 1:
			return True
		elif self.sensors.irArray.ir_value[1] < 2.32 or self.sensors.irArray.ir_value[4] < 2.32:
			return True
		elif self.sensors.irArray.ir_value[2] < 3.5 or self.sensors.ir_value[3] < 3.5
			return True
		return False

	def isLeftClear(self):
		return self.sensors.irArray.ir_value[0] < 1 and self.sensors.irArray.ir_value[1] < 2.32 and self.sensors.irArray.ir_value[2] < 3.5

	def isRightClear(self):
		return self.sensors.irArray.ir_value[5] < 1 and self.sensors.irArray.ir_value[4] < 2.32 and self.sensors.irArray.ir_value[3] < 3.5


	#flank maneuver attempts to calculate parameters that will allow us to make a triangle motion to the cube such that our turn towards the cube will be 90 degrees
	#this is somewhat of a simple algorithm, a more complex one would use our sensor lenght differences to perform more complex geometry. We do not have the time to research or derive such things.
	#returns True if our surroundings will let us start the flank maneuver, false if not
	def calculateFlankManeuver(self):
		hyp = self.ROBOT_RADIUS + self.sensors.camera.blockDistance - self.CAMERA_OFFSET
		opp = self.ROBOT_RADIUS + self.FLANK_APPROACH_LENGHT
		angle = math.asin(opp/hyp)
		if isLeftClear() == True:
			self.flank_first_angle = angle
		elif isRightClear() == True:
			self.flank_first_angle = -angle
		else:
			return False
		self.flank_target_distance = math.sqrt(hyp**2-opp**2)
		self.flank_actual_distance = 0
		return True

