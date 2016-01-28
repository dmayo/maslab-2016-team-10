from tamproxy.devices import Encoder
from math import pi

"""Encoder info: There are 4480 encoder ticks per revolution, which comes out to 2.875*pi inches"""
class EncoderWrap:
	def __init__(self,tamp):
		self.tamp=tamp
		self.encoderL = Encoder(self.tamp, 22, 23)
		self.encoderR = Encoder(self.tamp, 21, 20)
		self.isRobotMoving=False
		self.prevEncoderL=0
		self.pervEncoderR=0
		self.NOT_MOVING_EPSILON=62 #5 degrees of change

	def resetEncoders(self):
		self.encoderL.write(0)
		self.encoderR.write(0)

	def getDistanceTraveled(self):
		avg = (self.encoderL.val+self.encoderR.val)/2
		return avg/360.

	def update(self):
		if(abs(self.encoderL.val-self.prevEncoderL)<self.NOT_MOVING_EPSILON and abs(self.encoderL.val-self.prevEncoderL)<self.NOT_MOVING_EPSILON):
			self.isRobotMoving=False
		else:
			self.isRobotMoving=True
		self.prevEncoderL=self.encoderL.val
		self.prevEncoderR=self.encoderR.val
