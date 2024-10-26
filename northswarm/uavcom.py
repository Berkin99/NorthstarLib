#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import sys
sys.path.append('./')

import time
import northlib.ntrp as radioManager
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
import northlib.ntrp.ntrp as ntrp
from   northlib.ncmd.northcom import NorthCOM
from   math3d import *
import struct
import threading


class UavCOM(NorthCOM):
	
	UAV_IDLE     = 0
	UAV_MANUAL   = 1
	UAV_HEIGHT   = 2
	UAV_AUTO     = 3
	UAV_TAKEOFF  = 4
	UAV_LAND     = 5

	CMD_ID_UAV_CONTROLLER = 40

	def __init__(self, uri="radio:/0/76/2/E7E7E7E301"):
		super().__init__(uri)

		self.mode   = self.UAV_IDLE
		self.modeFunc = self._uavIdle
		self.uavThread = threading.Thread(target=self._uavTask, daemon=False)
		self.uavAlive = False

		self.position = [0.0, 0.0, 2.0] #Position Self Frame
		self.posBias  = [0.0, 0.0, 0.0] #Start Position
		self.heading  =  0.0            #Rotation Self Frame
		self.rc       = [0, 0, 0, 0, 0]

	def start(self):
		#self.connect() # Wait Connection Sync
		self.connection = True # 1 Way Connection, Not ideal 

		if self.connection is True:
			self.uavAlive = True

		self.uavThread.start()

	def setPosition(self, pos=list[float]): self.position = pos
	
	def setManual(self): self.setMode(self.UAV_MANUAL)
	
	def setAuto(self):
		if self.mode == self.UAV_IDLE: return
		self.setMode(self.UAV_AUTO)
	
	def takeOff(self):   self.setMode(self.UAV_TAKEOFF)
	def land(self):    	 self.setMode(self.UAV_LAND)
	def landForce(self): self.setMode(self.UAV_IDLE)

	def setMode(self, mode=int):
		modeDict = {
			self.UAV_IDLE    : self._uavIdle,
			self.UAV_MANUAL  : self._uavManual,
			self.UAV_HEIGHT  : self._uavHeight,
			self.UAV_AUTO    : self._uavAuto,
			self.UAV_TAKEOFF : self._uavTakeOff,
			self.UAV_LAND    : self._uavLand,
		}
		self.mode     = mode
		self.modeFunc = modeDict[mode]
		
	def setRC(self, channels=list[int]):
		self.rc = channels

	def setReference(self, pos=list[float]):
		refset = [1]
		refset.append(pos)
		self.SET("uavcom", refset)

	def _uavTask(self):
		while self.uavAlive:
			self.modeFunc()
			time.sleep(0.03)

	def _uavIdle(self):
		self.uavCMD([self.UAV_IDLE])
	
	def _uavManual(self):	
		arg = [self.UAV_MANUAL]
		arg.extend(self.rc)
		self.uavCMD(arg)
	
	def _uavAuto(self):
		arg = [self.UAV_AUTO]
		nav = vsub(self.position, self.posBias)
		arg.extend(struct.pack('<f', float(nav[0])))
		arg.extend(struct.pack('<f', float(nav[1])))
		arg.extend(struct.pack('<f', float(nav[2])))
		self.uavCMD(arg)
	
	def _uavHeight(self):
		arg = [self.UAV_HEIGHT]
		arg.extend(self.rc)
		self.uavCMD(arg)

	def _uavTakeOff(self):
		self.uavCMD([self.UAV_TAKEOFF])

	def _uavLand(self):
		self.uavCMD([self.UAV_LAND])

	def uavCMD(self, arg):
		""" IDLE    : [0]
		    MANUAL  : [1, roll, pitch, yaw, power]
		    HEIGHT  : [2, roll, pitch, yaw, posz[4]]
		    AUTO    : [3, posx[4], posy[4], posz[4]]
		    TAKEOFF : [4]
		    LAND    : [5] """
		self.txCMD(dataID = self.CMD_ID_UAV_CONTROLLER, channels = bytearray(arg))

	def destroy(self):
		self.setMode(self.UAV_IDLE)
		self.uavAlive = False
		return super().destroy()


uri = "radio:/2/76/2/E7E7E7E305",

if __name__ == '__main__':

	radioManager.radioSearch(baud=2000000) #Arduino DUE (USB Connection) has no Baudrate
	if not len(radioManager.availableRadios) >= 1: sys.exit()
	com = UavCOM(uri)
	com.start()

	# TODO: Make this IUavCOM object, full terminal commanded UAV
	while(1):
		parsed = input().split()
		if(parsed[0] == "AUTO")   : com.setAuto()
		if(parsed[0] == "TAKEOFF"): com.takeOff()
		if(parsed[0] == "LAND")   : com.land()
		if(parsed[0] == "IDLE")   : com.landForce()
		if(parsed[0] == "POS")    : com.setPosition([float(x) for x in parsed[1:]])

