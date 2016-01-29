from state import state
import wallFollowingState
import turnToBlockState
import lookingForBlocksState
import time
import timeout
import startState
import random

#substates: RandomTraveling, Turning, Scanning
#this state is NOT meant to be used if we are jammed. It will likely stay jammed when we turn. Use breakFreeState instead.

class RandomTravelingState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(RandomTravelingState, self).__init__(sensors, actuators, motorController, timer, utils)
		print "Starting RandomtTravelingState..."
		self.timeout = timeout.Timeout(30)
		self.substate = "RandomTraveling"
		self.TURN_SPEED = 40
		self.DRIVE_SPEED = 40
		self.SIDE_COLLISION_DISTANCE = 1
		self.FRONT_COLLISION_DISTANCE = 3.5 #meant to prevent the worst case: we head into a 90-degree angle and it gets inside our front opening, jamming us.
		self.RANDOM_ANGLE_RANGE = 35 #randomness of 30 degrees, to avoid bouncing back and forth between two walls
		self.lastTurnNegative = False
		self.intialGyroAngle = 0

		random.seed(time.time())


	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				if self.timeout.isTimeUp() == True:
					print 'State Timeout has timed out. Going to StartState...'
					return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				if self.sensors.uIR.val == 0:
					print 'Break beam has sensed a block. Going to Pick Up Block State...'
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
			
				if self.substate == "RandomTraveling":
					angleToTurn = self.checkCollisionAngle()
					if angleToTurn is not None:
						print 'We have collided. Bouncing off a random angle, ', angleToTurn, ' degrees...'
						if angleToTurn < 0:
							self.lastTurnNegative = True
						else:
							self.lastTurnNegative = False
						self.driveStraight(0)
						self.turnNDegreesSlowly(random.randrange(angleToTurn - self.RANDOM_ANGLE_RANGE,angleToTurn + self.RANDOM_ANGLE_RANGE))
						self.substate = "Turning"
					else:
						self.turnConstateRate(0,"Right")
						self.driveStraight(self.DRIVE_SPEED)
						if self.sensors.camera.detectBlock:
							print 'Block Detected. Turning to it...'
							return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				elif self.substate == "Turning":
					if self.hasFinishedTurning():
						if self.isStillColliding():
							print 'After turn, we are still colliding. Will start scanning for an open spot...'
							self.substate = "Scanning"
							self.intialGyroAngle = self.sensors.gyro.gyroCAngle
							if self.lastTurnNegative:
								self.turnConstateRate(self.TURN_SPEED,"Right")
							else:
								self.turnConstateRate(self.TURN_SPEED,"Left")
						else:
							print 'Not colliding anymore...'
							self.turnConstateRate(0,"Right")
							self.driveStraight(self.DRIVE_SPEED)
							self.substate = "RandomTraveling"
				elif self.substate == "Scanning":
					if self.isStillColliding() == False:
						print 'Finally found an open spot...'
						self.driveStraight(self.DRIVE_SPEED)
						self.turnConstateRate(0,"Right")
						self.substate = "RandomTraveling"
					elif (self.lastTurnNegative) and (self.sensors.gyro.gyroCAngle < (self.intialGyroAngle - 360)):
						print 'Not good. After full rotation, we cannot find an open spot. I guess we can go to start state and see what wall following can do? (We made a full rotation, so we are not jammed.)'
						return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					elif (self.lastTurnNegative == False) and (self.sensors.gyro.gyroCAngle > (self.intialGyroAngle + 360)):
						print 'Not good. After full rotation, we cannot find an open spot. I guess we can go to start state and see what wall following can do? (We made a full rotation, so we are not jammed.)'
						return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
				else:
					print 'Error! Substate ', self.substate, ' not a valid substate. Returning to StartState...'
					return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	#this is meant to serve as the mean of the random distro we will use to choose a rotation angle, to create a "bouncing" effect.
	def checkCollisionAngle(self):
		if self.checkIndividualSensor(0,self.SIDE_COLLISION_DISTANCE):
			return -90
		elif self.checkIndividualSensor(5,self.SIDE_COLLISION_DISTANCE):
			return 90
		elif self.checkIndividualSensor(1,self.SIDE_COLLISION_DISTANCE):
			return -120
		elif self.checkIndividualSensor(4,self.SIDE_COLLISION_DISTANCE):
			return 120
		elif self.checkIndividualSensor(2,self.FRONT_COLLISION_DISTANCE):
			return -160
		elif self.checkIndividualSensor(3,self.FRONT_COLLISION_DISTANCE):
			return 160
		else:
			return None

	def isStillColliding(self):
		if self.checkIndividualSensor(0,self.SIDE_COLLISION_DISTANCE):
			return True
		if self.checkIndividualSensor(1,self.SIDE_COLLISION_DISTANCE):
			return True
		if self.checkIndividualSensor(2,self.FRONT_COLLISION_DISTANCE):
			return True
		if self.checkIndividualSensor(3,self.FRONT_COLLISION_DISTANCE):
			return True
		if self.checkIndividualSensor(4,self.SIDE_COLLISION_DISTANCE):
			return True
		if self.checkIndividualSensor(5,self.SIDE_COLLISION_DISTANCE):
			return True
		return False