from PID import PID

class MotorController:
        """Encoder info: There are 4480 encoder ticks per revolution, which comes out to 2.875 inches"""
        encoder_epsilon = 62 #5 degrees of change
        
	def __init__(self,sensors,actuators):
		self.sensors=sensors
		self.actuators=actuators

		#PID
		self.PID=PID(.5, 1, 0.15)

		self.currentAngle=0
		self.desiredAngle=0
		self.motorLdrive=0
		self.motorRdrive=0
		self.fwdVel=0

		self.wallFollowPIDResult=0
		self.turnConstantRate=0

		self.motorState="turnToAngle"

	def stop(self):
		self.actuators.motorL.write(1,0)
		self.actuators.motorR.write(1,0)

	def updateMotorSpeeds(self):
		if(self.motorState=="turnToAngle"):
			self.updateTurnToAngle()
		elif(state.motorState=="wallFollow"):
			self.updateWallFolow()
		elif(state.motorState=="turnConstantRate"):
			self.updateTurnConstantRate()  

	def updateTurnToAngle(self):
		pidResult=self.PID.valuePID(self.sensors.gyro.gyroCAngle, self.desiredAngle)

		# print 'Angle Dif: ' + str(cAngle-self.initAngle) + '\tPID RESULT: '+ str(pidResult)
		# print 'Encoders:\tR: ' + str(self.encoderR.val) + '\tL: ' + str(self.encoderL.val)
		# print 'AVG: ' + str((self.encoderR.val + self.encoderL.val)/2.)

		self.motorLdrive = self.fwdVel - pidResult
		self.motorRdrive = self.fwdVel + pidResult

		self.actuators.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
		self.actuators.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

	def updateWallFollow(self):
		self.motorLdrive = self.fwdVel - wallFollowPIDResult
		self.motorRdrive = self.fwdVel + wallFollowPIDResult

		self.actuators.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
		self.actuators.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

	def updateTurnConstantRate(self):
		self.motorLdrive = -self.turnConstantRate
		self.motorRdrive = self.turnConstantRate

		self.actuators.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
		self.actuators.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))

