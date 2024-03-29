from PID import PID

class state(object):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		self.sensors=sensors
		self.actuators=actuators
		self.motorController=motorController
		self.timer=timer
		self.utils=utils
		self.ANGLE_EPSILON=1

	def run(self):
		raise "run not implemented in state"

	def getAngle(self):
		return self.sensors.gyro.gyroCAngle

	def isTurning():
		return False

	def isFinishedTurning(self):
		if(abs(self.motorController.desiredAngle-self.sensors.gyro.gyroCAngle)<self.ANGLE_EPSILON ans self.sensors.encoders.isRobotMoving==False):
			return True
		else:
			return False

	def turnNDegreesSlowly(self, turnAngle):
		self.motorState="turnToAngle"
		self.motorController.fwdVel=0
		self.motorController.desiredAngle=self.sensors.gyro.gyroCAngle+turnAngle
		'''
	    enum turningStates {turning,turned};
	    static turningStates myState = turning;
	    static long long int startTimeState;
	    static double startAngle;
	    turnedNDegreesSlowly=true;


	    if(!turningNDegreesSlowly){
	        finishedTurningNDegreesSlowly=0;
	        startTimeState = getTimeMicroseconds();
	        myState=turning;
	        startAngle=getAngle();
	    }
	    long long int difTime;
	    double difAngle;
	    difTime=(getTimeMicroseconds()-startTimeState)/1000;
	    difAngle= getAngle()- startAngle;
	    switch(myState){
	    case turning:
	        if(!finishedTurningNDegreesSlowly){
	            if (((difAngle>=angle)&&(angle>=0))||((difAngle<=angle)&&(angle<=0))){
	                finishedTurningNDegreesSlowly=1;
	                turnedNDegreesSlowly=0;
	                myState=turned;
	                setCarrotPosition(0,0);
	            }
	            else if(difTime>TURN_N_DEGREES_SLOWLY_TIMEOUT_MS){
	                myState=turned;
	                turnedNDegreesSlowly=0;
	                finishedTurningNDegreesSlowly=1;

	            }
	            else{
	                if(angle>0)
	                    turnToTheRightSlowly();
	                else
	                    turnToTheLeftSlowly();
	            }
	        }
	        break;
	    case turned:
	        break;
	    }
	    '''

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
		if self.sensors.color.c > 800 and self.actuators.sorter.sorterState=="None":
			if self.sensors.color.r > self.sensors.color.g:
				self.actuators.sorter.moveSorterLeft()
			else:
				self.actuators.sorter.moveSorterRight()
			return True
		else:
			return False


	def wallFollow(self, side):
		self.motorController.motorState="wallFollow"
		self.IRPID = PID(10, 5, .15)

		ir = self.sensors.irArray.ir_value
		if(side=="Left"):
			avg=self.sensors.irArray.getAvgDistanceLeftWall()
			min_val=self.sensors.irArray.getMinDistanceLeftWall()
		elif(side=="Right"):
			avg=self.sensors.irArray.getAvgDistanceRightWall()
			min_val=self.sensors.irArray.getMinDistanceRightWall()
		assert side=="Left" or side=="Right"

		#TODO:make this code better
		if avg != float('inf'):
			pidResult= -self.IRPID.valuePID(4, avg)
		elif min_val != float('inf'):
			pidResult= -self.IRPID.valuePID(4, min_val)
		else:
			pidResult = -20

		if self.sensors.irArray.ir_value[self.sensors.irArray.IRs[side][2]] < 4:
			pidResult = 20
			self.motorController.fwdVel = 0
		else:
			self.motorController.fwdVel = 30

		if(side=="Right"):
			pidResult*=-1

		self.motorController.wallFollowPIDResult = pidResult

	def turnConstantRate(self,turnSpeed):
		self.motorController.turnConstantRate=turnSpeed
		self.motorController.motorState="turnConstantRate"


