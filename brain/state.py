class state(object):
	def __init__(self, sensors, actuators, motorController, timer):
		self.sensors=sensors
		self.actuators=actuators
		self.motorController=motorController
		self.timer=timer

		self.finishedTurningNDegreesSlowly=False

		#constants
		TURN_SLOWLY_ANGLE=2

	def run(self):
		raise "run not implemented in state"

	def getAngle(self):
		return self.sensors.gyro.val

	def turnNDegreesSlowly(self, turnAngle):
		self.finishedTurningNDegreesSlowly=True
		self.motorController.desiredAngle=self.sensors.gyroCAngle+turnAngle
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
		setCarrotPosition(0, TURN_SLOWLY_ANGLE)

	def turnToTheLeftSlowly(self):
		setCarrotPosition(0, -1*TURN_SLOWLY_ANGLE)

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