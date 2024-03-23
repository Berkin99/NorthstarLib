import sys
sys.path.append('./')

import time
import northlib.ntrp as radioManager
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
import northlib.ntrp.ntrp as ntrp
import northlib.ncmd.controller as ncmd

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000) #Arduino DUE (USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()

    ctrl = ncmd.Controller() #Joystick controller
    time.sleep(1)
    
    rf_pipe = NorthNRF(0,0,address="E7E7E7E301") 
    print("RF Radio ID = " + str(ord(rf_pipe.id)))
    
    while 1: 
        #if ctrl.isAlive == False : break
        rf_pipe.txCMD(ctrl.getAxis())
        if not rf_pipe.radio.isRadioAlive(): break

    ctrl.destroy()
    radioManager.closeAvailableRadios()
    
    print("app exit")
    sys.exit()
