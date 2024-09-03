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
from   shape import Shape

import keyboard
import threading

class UavClient():
	def __init__(self, uris = list[str]):
		self.comList = list[UavCOM]([])
		for uri in uris: self.comList.append(UavCOM(uri))
		self.startAll()

	def startAll(self):
		for com in self.comList: com.start()	

	def setPositions(self, pList):
		for i in range(len(self.comList)):
			self.comList[i].setPosition(pList[i])

	def setAutoAll(self):
		for com in self.comList: com.setAuto()

	def takeOffAll(self):
		for com in self.comList: com.takeOff()

	def landAll(self):
		for com in self.comList: com.land()

	def landForce(self):
		for com in self.comList: com.landForce()

	def commandParser(self, string = str):
		parsed = string.split(' ')
		if(len(parsed) < 1): return
		com = None
		if(parsed[0] == "AUTO")   : self.setAutoAll()
		if(parsed[0] == "TAKEOFF"): self.takeOffAll()
		if(parsed[0] == "LAND")   : self.landAll()
		if(parsed[0] == "IDLE")   : self.landForce()
		
		if(parsed[0] == "0")      : com = self.comList[0]
		if(parsed[0] == "1")      : com = self.comList[1]
		if(parsed[0] == "2")      : com = self.comList[2]
		
		if com is None : return
		if(len(parsed) < 2): return

		if(parsed[1] == "POS")    : com.setPosition([float(x) for x in parsed[1:]])
		if(parsed[1] == "AUTO")   : com.setAuto()
		if(parsed[1] == "TAKEOFF"): com.takeOff()
		if(parsed[1] == "LAND")   : com.land()
		if(parsed[1] == "IDLE")   : com.landForce() 

uris = [
	"radio:/0/76/2/E7E7E7E301",
	"radio:/1/76/2/E7E7E7E303",
]

if __name__ == '__main__':
	
	radioManager.radioSearch (baud=2000000) #Arduino DUE (USB Connection) has no Baudrate
	if not len(radioManager.availableRadios) > 0: sys.exit()
	time.sleep(1)
	client = UavClient(uris)

	client.commandParser(input())
	while (1):
		client.commandParser(input())
	