
import serial
import time
import pygame
from pygame.locals import *


def commander():
    ser = serial.Serial('COM16',9600)

    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() < 1:return
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    L3 = [0,0]
    R3 = [0,0]
    try: 
        while(1):
            for event in pygame.event.get():
                if event.type == JOYAXISMOTION:
                    if event.axis == 0:  # X ekseni (L3)
                        L3[0] = int(joystick.get_axis(0)*127)
                    elif event.axis == 1:  # Y ekseni (L3)
                        L3[1] = int(joystick.get_axis(1)*127)
                    elif event.axis == 2:  # X ekseni (R3)
                        R3[0] = int(joystick.get_axis(2)*127)
                    elif event.axis == 3:  # Y ekseni (R3)
                        R3[1] = int(joystick.get_axis(3)*127)
            msg = str(L3[0])+":"+str(L3[1])+":"+str(R3[0])+":"+str(R3[1])
            print(msg)
            ser.write(msg.encode())
            time.sleep(0.03)
    except serial.SerialException as e:
        pass
    pygame.quit()




commander()