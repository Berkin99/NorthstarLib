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
from northlib.ntrp.northpipe import NorthPipe

__author__ = 'Yeniay RD'
__all__ = ['Controller']

class Controller():
    """ 
    NTRP Joystick Controller 
    """
    
    def __init__(self,pipe):

        self.pipe = pipe
        pygame.init()
        pygame.joystick.init()
        self.isAlive = False
        self.axis = [0,0,0,0]

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)  # First Founded JOYSTICK 
            self.joystick.init()
            self.isAlive = True
            self.ctrlThread = threading.Thread(target=self.ctrlProcess,daemon=False)
            self.ctrlThread.start()

        else: print("NPX:/> Joystick Not Found.")

    def ctrlProcess(self):
        while self.isAlive:
            pygame.event.pump()  # Only Joystick process
            for i in range(4):
                self.axis[i] = (int)(((self.joystick.get_axis(i)+1)*255)/2)

            #print(self.axis)
            self.pipe.txCMD(bytearray(self.axis))
            time.sleep(0.01)
       
    def destroy(self):
        self.isAlive = False