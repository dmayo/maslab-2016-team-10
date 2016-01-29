from PID import PID

class state(object):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		self.sensors=sensors
		self.actuators=actuators
		self.motorController=motorController
		self.timer=timer
		self.utils=utils
		self.ANGLE_EPSILON=1
		self.MIN_FRONT_WALL_DIST=4

	def run(self):
		raise "run not implemented in state"

	def getAngle(self):
		return self.sensors.gyro.gyroCAngle

	def isTurning():
		return False

	def isFinishedTurning(self):
		if(abs(self.motorController.desiredAngle-self.sensors.gyro.gyroCAngle)<self.ANGLE_EPSILON and self.sensors.encoders.isRobotMoving==False):
			return True
		else:
			return False

	def turnNDegreesSlowly(self, turnAngle):
		self.motorController.motorState="turnToAngle"
		self.motorController.fwdVel=0
		self.motorController.desiredAngle=self.sensors.gyro.gyroCAngle+turnAngle

	def turnNDegreesAndMove(self, turnAngle, speed):
		self.motorController.motorState="turnToAngleAndMove"
		self.motorController.fwdVel=speed
		self.motorController.desiredAngle=self.sensors.gyro.gyroCAngle+turnAngle

	def turnToTheRightSlowly(self):
		#setCarrotPosition(0, TURN_SLOWLY_ANGLE)
		pass

	def turnToTheLeftSlowly(self):
		#setCarrotPosition(0, -1*TURN_SLOWLY_ANGLE)
		pass

	def foundCube(self):
		pass

	def detectedCube(self):
		pass

	def getDistanceNearestCube(self):
		pass

	def getAngleNearestCube(self):
		pass

	def setCarrotPosition(self, distance, angle):

		#desiredAngle= getNewAngle() + angle;
		#desiredPosition = getNewPosition() +radiusInInches;
		pass

	#returns TRUE if a block was found, FALSE if not
	def sortBlock(self):
		if self.utils.ourBlockColor=="Red":
			otherBlockColor="Green"
		elif self.utils.ourBlockColor=="Green":
			otherBlockColor="Red"
		assert self.utils.ourBlockColor=="Red" or self.utils.ourBlockColor=="Green"

		if self.sensors.color.getBlockColor()==self.utils.ourBlockColor:
			self.actuators.sorter.moveSorterLeft()
			return True
		elif self.sensors.color.getBlockColor()==otherBlockColor:
			self.actuators.sorter.moveSorterRight()
			return True
		else:
			return False

	def wallFollow(self, side, speed):
		self.motorController.motorState="wallFollow"
		self.IRPID = PID(10, 5, .15)
		fwdVel=0
		otherSide=""
		pidResult=0

		ir = self.sensors.irArray.ir_value
		if(side=="Left"):
			otherSide="Right"
			avg=self.sensors.irArray.getAvgDistanceLeftWall()
			min_val=self.sensors.irArray.getMinDistanceLeftWall()
		elif(side=="Right"):
			otherSide="Left"
			avg=self.sensors.irArray.getAvgDistanceRightWall()
			min_val=self.sensors.irArray.getMinDistanceRightWall()
		assert side=="Left" or side=="Right"


		#cases:
		#no wall detected
		#one sensor detects wall
		#both sensors detect wall
		#cases of things the sensors could be seeing:
		#nothing
		#flat wall
		#wall corner
		#sack of blocks


		#both sensors see something
		if avg != float('inf'):
			if (self.sensors.ir_array.isFlatWall(side)):
				pidResult=self.followWall(side, avg)
				fwdVel=speed
			if (self.sensors.ir_array.getWallInFrontDistance(side)<self.MIN_FRONT_WALL_DIST):
				#turn to avoid hitting wall in front
				self.turnConstantRate(30,otherSide)

			'''
			elif (self.sensors.ir_array.isCorner(side)):
				pass
			elif (self.sensors.ir_array.isCliff(side)):
				pass
			'''
		#one sensor sees something
		elif min_val != float('inf'):
			if (self.sensors.ir_array.getWallInFrontDistance(side)<self.MIN_FRONT_WALL_DIST):
				#turn to avoid hitting wall in front
				self.turnConstantRate(30,otherSide)
			else:
				pidResult=self.followWall(side,min_val)
		#both sensors don't see anything
		else:
			lookForWall()
			pidResult = -20

		self.motorController.wallFollowPIDResult = pidResult
		self.motorController.fwdVel=fwdVel

	def lookingForWall(self):
		pass

	def rotateWithWall(self):
		pass

	def followWall(self,side,avg):
		pidResult=-self.IRPID.valuePID(4, avg)
		if(side=="Right"):
			pidResult*=-1
		return pidResult

	#substates: lookingForWall, rotate, followingWall


	def turnConstantRate(self,turnSpeed,direction):
		self.motorController.turnConstantRate=turnSpeed
		self.motorController.turnConstantRateDirection=direction
		self.motorController.motorState="turnConstantRate"

	def driveStraight(self,speed):
		self.motorController.fwdVel=speed
		self.motorController.motorState="driveStraight"


