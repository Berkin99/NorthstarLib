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
import northlib.ntrp.ntrp as ntrp
import northlib.ncmd.controller as ncmd
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
from   northlib.ncmd.northcom  import NorthCOM
from   northlib.ncmd.nrxtable  import NrxTableLog
from   northswarm.uavcom import UavCOM

# Import helpers from this package so running as a module works
from northswarm.shape import *
from northswarm.math3d import *

import time
import threading

class UavClient():
	def __init__(self, uris = list[str], spos=list):
		self.rc = ncmd.Controller(True) # Joystick controller
		self.comList = list[UavCOM]([])
		self.operation = False
		for uri in uris: self.comList.append(UavCOM(uri))

		for i in range(len(spos)):
			if i >= len(self.comList): break 
			self.comList[i].posBias = spos[i]
			self.comList[i].position = vadd([0, 0, 2], spos[i])
		self.startAll()

	def operationLock(self):
		self.operation = False

	def operationUnlock(self):
		self.operation = True

	def setOperation(self, shp1, shp2, interval):
		i = 0
		while i < interval:
			if self.operation == False: break
			sh = shapeLerp(shp1, shp2, i / interval)
			self.setPositionAll(sh.getPoints())
			i += 0.05 
			time.sleep(0.05)
	
	def operationThread(self):
		op1 = Shape([0, 0,  5],  [0, 0, 0],   2, Triangle)
		op2 = Shape([0, 0, 13],  [0, 0, 270], 2, Triangle)
		op3 = Shape([0, 0, 13],  [0, 0, 360], 2.5, Triangle)
		op4 = Shape([13, 0, 12], [0, 0, 0],   1, Trimap )
		op5 = Shape([13, 0, 12], [0, 0, 720], 1, Trimap )
		
		self.operationUnlock()
		client.takeOffAll()
		
		if self.operation == False: return
		time.sleep(1)
		client.setAutoAll()
		client.setOperation(op1, op2, 20)
		client.setOperation(op2, op3, 10)
		time.sleep(5)

		self.setPositionAll(op4.getPoints())
		if self.operation == False: return
		time.sleep(5)
		client.setOperation(op4, op5, 100)
		
		if self.operation == False: return
		time.sleep(8)
		client.landAll()

	def setPosition(self, pos):
		if len(pos) < 3: return
		try:
			for i in range(len(self.comList)):
				self.comList[i].setPosition(vadd(self.comList[i].posBias, pos))
		except: ValueError

	def startAll(self):
		for com in self.comList: 
			com.start()	
			time.sleep(0.01)

	def setAutoAll(self):
		print("AutoALL")
		for com in self.comList: com.setAuto()

	def setPositionAll(self, pCloud):
		print(pCloud) 
		for i in range(len(pCloud)):
			if(i >= len(self.comList)): break
			self.comList[i].setPosition(pCloud[i])

	def takeOffAll(self):
		print("TakeoffALL")
		for com in self.comList: com.takeOff()

	def landAll(self):
		print("LandALL")
		for com in self.comList: com.land()

	def landForce(self):
		for com in self.comList: com.landForce()

	def setHome(self):
		for com in self.comList: com.setPosition(vadd(com.posBias, [0, 0, 2]))

	def commandParser(self, string = str):
		parsed = string.split(' ')
		if(len(parsed) < 1): return
		com = None

		if(parsed[0] == "UNLOCK"):
			self.opPcs = threading.Thread(target=self.operationThread, daemon=False)
			self.opPcs.start()

		if(parsed[0] == "LOCK"): self.operationLock()

		if(parsed[0] == "AUTO")   : self.setAutoAll()
		if(parsed[0] == "TAKEOFF"): self.takeOffAll()
		if(parsed[0] == "LAND")   : self.landAll()
		if(parsed[0] == "IDLE")   : self.landForce()
		if(parsed[0] == "POS")    : self.setPosition([float(x) for x in parsed[1:]])
		if(parsed[0] == "HOME")   : self.setHome()

		if(parsed[0] == "NAV0")   : self.setPositionAll([[-3,  0,  14], [0,  5,  14],  [3,  0,  14]])
		if(parsed[0] == "NAV1")   : self.setPositionAll([[12,  0,  15], [15, 5,  15],  [17, 0,  15]])

		if(parsed[0] == "0")      : com = self.comList[0]
		if(parsed[0] == "1")      : com = self.comList[1]
		if(parsed[0] == "2")      : com = self.comList[2]
		
		if com is None : return
		if(len(parsed) < 2): return

		if(parsed[1] == "POS")     : com.setPosition([float(x) for x in parsed[1:]])
		if(parsed[1] == "HOME")    : com.setPosition(vadd([0, 0, 3], com.posBias))
		if(parsed[1] == "AUTO")    : com.setAuto()
		if(parsed[1] == "TAKEOFF") : com.takeOff()
		if(parsed[1] == "LAND")    : com.land()
		if(parsed[1] == "IDLE")    : com.landForce()
		if(parsed[1] == "MANUAL")  : 
			self.rc.callBack = lambda x : com.setRC(channels = x) 
			com.setManual()

uris = [
	"radio:/0/76/2/E7E7E7E301",
	"radio:/1/76/2/E7E7E7E303",
	"radio:/2/76/2/E7E7E7E305",
]

spos = [[-3, 0, 0], [0, 5, 0], [3, 0, 0]]

if __name__ == '__main__':

	radioManager.radioSearch(baud=2000000)
	if not len(radioManager.availableRadios) >= len(uris): sys.exit()
	time.sleep(1)
	client = UavClient(uris, spos)

	print("Commands ON")
	while (1):
		client.commandParser(input())