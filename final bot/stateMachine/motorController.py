from PID import PID

class MotorController:        
	def __init__(self,sensors,actuators):
		self.sensors=sensors
		self.actuators=actuators

		#PID
		self.PID=PID(1, 2, 0.15)

		self.currentAngle=0
		self.desiredAngle=0
		self.motorLdrive=0
		self.motorRdrive=0
		self.fwdVel=0

		self.wallFollowPIDResult=0
		self.turnConstantRate=0

		self.motorState="turnToAngle"
	#fix this
	def stop(self):
		self.actuators.motorL.write(1,0)
		self.actuators.motorR.write(1,0)

	def updateMotorSpeeds(self):
		#print self.motorState
		if(self.motorState=="turnToAngle"):
			self.updateTurnToAngle()
		elif(self.motorState=="wallFollow"):
			self.updateWallFollow()
		elif(self.motorState=="turnConstantRate"):
			self.updateTurnConstantRate()
		elif(self.motorState=="driveStraight"):
			self.updateTurnConstantRate()  

	def updateTurnToAngle(self):
		pidResult=self.PID.valuePID(self.sensors.gyro.gyroCAngle, self.desiredAngle)

		# print 'Angle Dif: ' + str(cAngle-self.initAngle) + '\tPID RESULT: '+ str(pidResult)
		# print 'Encoders:\tR: ' + str(self.encoderR.val) + '\tL: ' + str(self.encoderL.val)
		# print 'AVG: ' + str((self.encoderR.val + self.encoderL.val)/2.)

		self.motorLdrive = pidResult
		self.motorRdrive = pidResult

		self.actuators.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
		self.actuators.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

	def updateWallFollow(self):
		self.motorLdrive = self.fwdVel - self.wallFollowPIDResult
		self.motorRdrive = self.fwdVel + self.wallFollowPIDResult

		self.actuators.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
		self.actuators.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

	def updateTurnConstantRate(self):
		self.motorLdrive = -self.turnConstantRate
		self.motorRdrive = self.turnConstantRate

		self.actuators.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
		self.actuators.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

	def updateDriveStraight(self):
		self.motorLdrive = self.fwdVel - pidResult
		self.motorRdrive = self.fwdVel + pidResult

		self.actuators.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
		self.actuators.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

