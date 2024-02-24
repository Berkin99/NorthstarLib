#!/usr/bin/env pythonh
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import threading
import pygame
import time
import northlib.ntrp
from northlib.ntrp.northradio import NorthRadio
from northlib.ntrp.northpipe import NorthPipe

__author__ = 'Yeniay RD'
__all__ = ['Controller']

class Controller():
    def __init__(self,pipe=NorthPipe):
        #Set UAV Mode to CONTROLLER
        #Wait ACK Message withtimeout
        self.pipe = pipe
        pygame.init()
        pygame.joystick.init()
        self.isAlive = False
        self.axis = [0,0,0,0]

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)  # İlk joystick'i alır
            self.joystick.init()
            self.isAlive = True
            self.controlThread = threading.Thread(target=self.controlProcess,daemon=False)
            self.controlThread.start()
            
        else: print("Controller Not Found.")

    def controlProcess(self):
        ch_arr = bytearray(4)
        while self.isAlive:
            pygame.event.pump()  # Sadece joystick eventlerini işler, diğerlerini ihmal eder
            for i in range(4):
                self.axis[i] = (int)(((self.joystick.get_axis(i)+1)*255)/2)
                ch_arr = bytearray(self.axis)
                self.pipe.transmitCMD(ch_arr)
                time.sleep(0.03)

            print(self.axis)
            #self.pipe.transmitCMD(self.axis)
            #time.sleep(0.4)
            
    def destroy(self):
        self.isAlive = False