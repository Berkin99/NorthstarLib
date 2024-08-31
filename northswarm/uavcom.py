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
import northlib.ncmd.controller as ncmd
from   northlib.ncmd.northcom import NorthCOM
from   northlib.ncmd.nrxtable import NrxTableLog
import keyboard
import threading


class UavCOM(NorthCOM):
	
	UAV_IDLE     = 0
	UAV_HEIGHT   = 1
	UAV_NAV      = 2

	def __init__(self, uri="radio:/0/76/2/E7E7E7E301"):
		super().__init__(uri)

	def process(self):
		self.connect()
		self.synchronize()

	def setTarget(self, target = list):
		if len(target) < 3 : return
		self.SET("cpos", [])

	def setMode(self, mode):
		self.txCMD()

	def takeOff(self):
		pass

	def land(self):
		pass

	def destroy(self):
		return super().destroy()