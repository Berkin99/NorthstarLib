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

    #ctrl = ncmd.Controller() #Joystick controller
    time.sleep(1)
    
    uavcom = NorthNRF(address="E7E7E7E301")

    while 1:
        if uavcom.radio.isRadioAlive()==False : break 
        #if ctrl.isAlive == False : break

        #uavcom.txCMD(channels=ctrl.getAxis(),force=True)
        time.sleep(0.05)


    #ctrl.destroy()
    uavcom.destroy()
    radioManager.closeAvailableRadios()
    
    print("rc commander exit")
    time.sleep(0.1)
    sys.exit()
