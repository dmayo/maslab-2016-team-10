from PID import PID
import math

class state(object):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		self.sensors=sensors
		self.actuators=actuators
		self.motorController=motorController
		self.timer=timer
		self.utils=utils
		self.ANGLE_EPSILON=1
		self.MIN_FRONT_WALL_DIST=5
		self.WALL_FOLLOW_SENSOR_CAP = 24
		self.WALL_FOLLOW_ROTATE_SPEED = 30
		self.WALL_FOLLOW_SLOW_SPEED = 10
		self.MAX_WALL_FOLLOW_TURN_SPEED=40

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

	def wallFollow(self, side, speed, wfPID):
		self.motorController.motorState="wallFollow"
		pidResult=0
		avg = 0

		"""ir = self.sensors.irArray.ir_value
		if(side=="Left"):
			otherSide="Right"
			avg=self.sensors.irArray.getAvgDistanceLeftWall()
			min_val=self.sensors.irArray.getMinDistanceLeftWall()
		elif(side=="Right"):
			otherSide="Left"
			avg=self.sensors.irArray.getAvgDistanceRightWall()
			min_val=self.sensors.irArray.getMinDistanceRightWall()
		assert side=="Left" or side=="Right"""

		#if we are blocked in front, turn in place until we are free to move again:
		if (self.checkIndividualSensor(2,self.MIN_FRONT_WALL_DIST) or self.checkIndividualSensor(3,self.MIN_FRONT_WALL_DIST)):
			if side=="Left":
				self.turnConstantRate(self.WALL_FOLLOW_ROTATE_SPEED,"Right")
			elif side=="Right":
				self.turnConstantRate(self.WALL_FOLLOW_ROTATE_SPEED,"Left")
			wfPID.resetPID()
			return #nothing else necessary

		leftSide = self.sensors.irArray.ir_value[0]
		leftAngle = self.sensors.irArray.ir_value[1]
		leftFront = self.sensors.irArray.ir_value[2]
		rightFront = self.sensors.irArray.ir_value[3]
		rightAngle = self.sensors.irArray.ir_value[4]
		rightSide = self.sensors.irArray.ir_value[5]

		if (side=="Left"):
			#check: are both left sensors infinite?
			if math.isinf(leftSide) and math.isinf(leftAngle):
				#if so, are all the other sensors infinite?
				if math.isinf(leftFront) and math.isinf(rightFront) and math.isinf(rightAngle) and math.isinf(rightSide):
					self.driveStraight(speed)
				else:
					self.turnConstantRate(self.WALL_FOLLOW_ROTATE_SPEED,"Left")
				wfPID.resetPID()
				return #noPID
			else:
				if math.isinf(leftSide):
					leftSide = self.WALL_FOLLOW_SENSOR_CAP
				if math.isinf(leftAngle):
					leftAngle = self.WALL_FOLLOW_SENSOR_CAP
				adjusted_left_Angle = (leftAngle*math.cos(math.radians(30))) - 7.5 + 7.5*math.cos(math.radians(30))
				avg = (leftSide+adjusted_left_Angle)/2

		elif (side=="Right"):
			#check: are both left sensors infinite?
			if math.isinf(rightSide) and math.isinf(rightAngle):
				#if so, are all the other sensors infinite?
				if math.isinf(leftFront) and math.isinf(rightFront) and math.isinf(leftAngle) and math.isinf(leftSide):
					self.driveStraight(speed)
				else:
					self.turnConstantRate(self.WALL_FOLLOW_ROTATE_SPEED,"Right")
				wfPID.resetPID()
				return #noPID
			else:
				if math.isinf(rightSide):
					rightSide = self.WALL_FOLLOW_SENSOR_CAP
				if math.isinf(rightAngle):
					rightAngle = self.WALL_FOLLOW_SENSOR_CAP
				adjusted_right_Angle = (rightAngle*math.cos(math.radians(30))) - 7.5 + 7.5*math.cos(math.radians(30))
				avg = (rightSide+adjusted_right_Angle)/2

		pidResult=self.followWall(side,avg,wfPID)
		if pidResult < -self.MAX_WALL_FOLLOW_TURN_SPEED:
			pidResult = -self.MAX_WALL_FOLLOW_TURN_SPEED
		elif pidResult > self.MAX_WALL_FOLLOW_TURN_SPEED:
			pidResult = self.MAX_WALL_FOLLOW_TURN_SPEED
		self.motorController.wallFollowPIDResult = pidResult
		self.motorController.fwdVel=speed
		print 'PID result is: ', pidResult

				

		"""if(side=="Left"):
			side_sensor = self.sensors.irArray.ir_value[0]
			if math.isinf(side_sensor):
				side_sensor = self.WALL_FOLLOW_SENSOR_CAP
			angle_sensor = self.sensors.irArray.ir_value[1]
			if math.isinf(angle_sensor):
				angle_sensor = self.WALL_FOLLOW_SENSOR_CAP
			otherSide="Right"
			avg=self.sensors.irArray.getAvgDistanceLeftWall()
			min_val=self.sensors.irArray.getMinDistanceLeftWall()
		elif(side=="Right"):
			otherSide="Left"
			avg=self.sensors.irArray.getAvgDistanceRightWall()
			min_val=self.sensors.irArray.getMinDistanceRightWall()


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
			if (self.sensors.irArray.isFlatWall(side)):
				pidResult=self.followWall(side, avg)
				fwdVel=speed
			if (self.sensors.irArray.getWallInFrontDistance(side)<self.MIN_FRONT_WALL_DIST):
				#turn to avoid hitting wall in front
				self.turnConstantRate(30,otherSide)

			'''
			elif (self.sensors.irArray.isCorner(side)):
				pass
			elif (self.sensors.irArray.isCliff(side)):
				pass
			'''
		#one sensor sees something
		elif min_val != float('inf'):
			if (self.sensors.irArray.getWallInFrontDistance(side)<self.MIN_FRONT_WALL_DIST):
				#turn to avoid hitting wall in front
				self.turnConstantRate(30,otherSide)
			else:
				pidResult=self.followWall(side,min_val)
		#both sensors don't see anything
		else:
			lookForWall()
			#pidResult = -20"""

	def getAverageSideAndAngleSensors(self,sideSensor,angleSensor):
		projAngleSensor = angleSensor*math.cos(math.radians(30))
		return (projAngleSensor + sideSensor)/2

	def lookingForWall(self):
		self.driveStraight(30)

	def rotateWithWall(self):
		pass

	def followWall(self,side,avg,wfPID):
		pidResult=-wfPID.valuePID(4, avg)
		if(side=="Right"):
			pidResult*=-1
		return pidResult

	#substates: lookingForWall, rotate, followingWall


	def turnConstantRate(self,turnSpeed,direction):
		self.motorController.turnConstantRate=turnSpeed
		self.motorController.turnConstantRateDirection=direction
		self.motorController.motorState="turnConstantRate"

	def turnConstantRateAndMove(self,turnSpeed,moveSpeed,direction):
		self.motorController.turnConstantRate=turnSpeed
		self.motorController.turnConstantRateDirection=direction
		self.motorController.fwdVel = 0
		self.motorController.motorState="turnConstantRateAndMove"

	def driveStraight(self,speed):
		self.motorController.fwdVel=speed
		self.motorController.motorState="driveStraight"

	#collision detection avoids 1 inch of space on the sides. Trig was used to determine the lenght of the 30-degree angled sensors.
	#for the front sensors, we seek to avoid the worst case of a 90-degree angle, comes out to 2.9+.59 = about 3.5
	def isColliding(self):
		if self.checkIndividualSensor(0,.5):
			return True
		if self.checkIndividualSensor(1,1):
			return True
		if self.checkIndividualSensor(2,1.6):
			return True
		if self.checkIndividualSensor(3,1.6):
			return True
		if self.checkIndividualSensor(4,1):
			return True
		if self.checkIndividualSensor(5,.5):
			return True
		return False

	def checkIndividualSensor(self,pos,threshold):
		return (self.sensors.irArray.ir_value[pos] < threshold and self.sensors.irArray.ir_value[pos] > 0)


