from state import state
import startState
import checkForMoreBlocksState
from utils import *
import time
import lookingForBlocksState
import randomTravelingState
import timeout

#substates: WallDetect,FindSafeAngle,PickUpBlock

class PickUpBlockState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(PickUpBlockState, self).__init__(sensors, actuators, motorController, timer, utils)

		print "PickUpBlockState starting..."
		self.timeout = timeout.Timeout(15)
		self.pickupTimeout = timeout.Timeout(5)
		self.substate = "WallDetect"
		self.startAngle = 0
		self.pickUpBlockStartTime = 0

		#start off stationary
		self.driveStraight(0)

		self.SCAN_SPEED=30
		self.JOSTLE_TIMEOUT = 10 
		self.MIN_SAFE_DISTANCE = 5 #an approximation of the distance in inches we'd need to read from a 90-degree corner pointing at the middle of the robot to life the block safely
		self.motorController.fwdVel=0
	
	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				#State Timeout
				if self.timeout.isTimeUp() == True:
					print 'StateTimeout timed out in substate ', self.substate, '. Going to BreakFreeState...'
					return breakFreeState.BreakFreeState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				if self.substate == "WallDetect":
					if self.isItSafeToLiftArm() == True:
						print 'Safe to pick up arm. Starting pick up block procedure.'
						self.pickupTimeout.reset()
						self.actuators.arm.pickUpBlock()
						self.substate = "PickUpBlock"
					else:
						print 'Collision Info: Sensor 2', self.sensors.irArray.ir_value[2], ' sensor 3: ',self.sensors.irArray.ir_value[3]
						print 'Too close to pick up arm. Attempting to find better angle...'
						self.substate = "FindSafeAngle"
						self.initialAngle = self.sensors.gyro.gyroCAngle
				elif self.substate =="FindSafeAngle":
					if self.isItSafeToLiftArm() == True:
						print 'Collision Info: Sensor 2', self.sensors.irArray.ir_value[2], ' sensor 3: ',self.sensors.irArray.ir_value[3]
						print 'Found a good angle! Beginning pickup.'
						#self.turnConstantRate(0)
						self.pickupTimeout.reset() #this limits how long we wait before we start jostling
						self.timeout.reset() #and this limits how long we jostle for
						self.actuators.arm.pickUpBlock()
						self.substate = "PickUpBlock"
					elif self.sensors.gyro.gyroCAngle>(self.initialAngle+360):
						print 'After a full 360 could not find a good angle! Abandoning state...'
						#self.turnConstantRate(0)
						return randomTravelingState.RandomTravelingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					else:
						self.turnConstantRate(self.SCAN_SPEED, "Right")
				elif self.substate == "PickUpBlock":
					isBlockDetected = self.sortBlock()
					if isBlockDetected == True:
						print 'Block successfully thrown into funnel!'
						return lookingForBlocksState.LookingForBlocksState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					else:
						if self.pickupTimeout.isTimeUp() == True:
							if self.actuators.sorter.sorterState == "None":
									self.actuators.sorter.jostle()

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	def isItSafeToLiftArm(self):
		if self.checkIndividualSensor(2,self.MIN_SAFE_DISTANCE):
			return False
		if self.checkIndividualSensor(3,self.MIN_SAFE_DISTANCE):
			return False
		return True

