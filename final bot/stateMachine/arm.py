from tamproxy.devices import Servo
import time

class Arm:
	def __init__(self,tamp):
		self.tamp=tamp
		self.servo = Servo(self.tamp, 9)
		self.servo.bottom = 10 #5 for metal
		self.servo.top = 150
		self.servo.speed = 30
		self.servo.write(self.servo.bottom)
		self.servoval = self.servo.bottom
		self.delta = 0
		self.armState="None"
		self.nextArmState="None"

	def pickUpBlock(self):
		self.armState="Up"
		self.nextArmState="Down"

	def moveArmUp(self):
		if self.servoval <= self.servo.top: 
			self.delta = self.servo.speed
			self.armState="Up"
		else:
			self.setPause(.25)
			self.armState="Pause"
			#self.armState=self.nextArmState
			#self.nextArmState="None"

	def moveArmDown(self):
		if self.servoval > self.servo.bottom:
			self.delta = -self.servo.speed
			self.armState="Down"
		else:
			self.armState=self.nextArmState
			self.nextArmState="None"

	def setPause(self,pauseLength):
		self.startPauseTime=time.time()
		self.pauseLength=pauseLength

	def pauseArm(self):
		if(time.time()-self.startPauseTime>self.pauseLength):
			self.armState=self.nextArmState
			self.nextArmState="None"
			self.delta=0

	def update(self):
		if self.armState!="None":
			if self.armState=="Up":
				self.moveArmUp()
			elif self.armState=="Down":
				self.moveArmDown()
			elif(self.armState=="Pause"):
				self.pauseArm()
			self.servoval += self.delta
			if(self.servoval<0):
				self.servoval=0
			self.servo.write(abs(self.servoval))

