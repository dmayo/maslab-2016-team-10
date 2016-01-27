from PID import PID

class MotorController:
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

	def stop(self):
		self.actuators.motorL.write(1,0)
		self.actuators.motorR.write(1,0)

	def updateMotorSpeeds(self):
		pidResult=self.PID.valuePID(self.sensors.gyro.gyroCAngle, self.desiredAngle)

		# print 'Angle Dif: ' + str(cAngle-self.initAngle) + '\tPID RESULT: '+ str(pidResult)
		# print 'Encoders:\tR: ' + str(self.encoderR.val) + '\tL: ' + str(self.encoderL.val)
		# print 'AVG: ' + str((self.encoderR.val + self.encoderL.val)/2.)

		self.motorLdrive = self.fwdVel - pidResult
		self.motorRdrive = self.fwdVel + pidResult

		self.actuators.motorL.write(self.motorLdrive < 0,abs(self.motorLdrive))
		self.actuators.motorR.write(self.motorRdrive < 0,abs(self.motorRdrive))
