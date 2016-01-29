from state import state
import startState
import checkForMoreBlocksState
from utils import *
import time
import lookingForBlocksState
import randomTravelingState

#substates: WallDetect,FindSafeAngle,PickUpBlock

class PickUpBlockState(state):
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(PickUpBlockState, self).__init__(sensors, actuators, motorController, timer, utils)

		print "PickUpBlockState starting..."
		self.timeout = Timeout(15)
		self.pickupTimeout = Timeout(5)
		self.substate = "WallDetect"
		self.startAngle = 0
		self.pickUpBlockStartTime = 0

		#start off stationary
		self.motorController.fwdVel = 0
		self.motorController.turnConstantRate(0)

		self.SCAN_SPEED=3
		self.JOSTLE_TIMEOUT = 10 
		self.MIN_SAFE_DISTANCE = 9 #an approximation of the distance in inches we'd need to read from a 90-degree corner pointing at the middle of the robot to life the block safely

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
					if isItSafeToLiftArm() == True:
						print 'Safe to pick up arm. Starting pick up block procedure.'
						self.pickupTimeout.reset()
						self.actuators.arm.pickUpBlock()
						self.substate = "PickUpBlock"
					else:
						print 'Too close to pick up arm. Attempting to find better angle...'
						self.substate = "FindSafeAngle"
						self.initialAngle = self.sensors.gyro.gyroCAngle
				elif self.substate =="FindSafeAngle":
					if isItSafeToLiftArm() == True:
						print 'Found a good angle! Beginning pickup.'
						self.turnConstantRate(0)
						self.pickupTimeout.reset() #this limits how long we wait before we start jostling
						self.timeout.reset() #and this limits how long we jostle for
						self.actuators.arm.pickUpBlock()
						self.substate = "PickUpBlock"
					elif self.sensors.gyro.gyroCAngle>(self.initialAngle+360):
						print 'After a full 360 could not find a good angle! Abandoning state...'
						self.turnConstantRate(0)
						return randomTravelingState.RandomTravelingState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					else:
						self.turnConstantRate(self.SCAN_SPEED)
				elif self.substate == "PickUpBlock":
					isBlockDetected = self.sortBlock()
					if isBlockDetected == True:
						print 'Block successfully thrown into funnel!'
						return checkForMoreBlocksState.CheckForMoreBlocksState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)
					else:
						if self.pickupTimeout.isTimeUp() == True:
							if self.actuators.sorter.sorterState == "None":
									self.actuators.sorter.jostle()

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	def isItSafeToLiftArm(self):
		return (self.sensors.irArray.ir_value[2] < self.MIN_SAFE_DISTANCE and self.sensors.irArray.ir_value[3] < self.MIN_SAFE_DISTANCE)

