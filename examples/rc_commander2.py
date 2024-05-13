import sys
sys.path.append('./')

import time
import northlib.ntrp as radioManager
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
import northlib.ntrp.ntrp as ntrp
import northlib.ncmd.controller as ncmd
from northlib.ncmd.northcom import NorthCOM
from northlib.ncmd.nrxtable import NrxTableLog



uri =  "radio:/0/76/2/E7E7E7E301"

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000)    #Arduino DUE (USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()

    ctrl = ncmd.Controller(True) #Joystick controller
    time.sleep(1)
    
    uavcom = NorthCOM(uri=uri)
    uavcom.connect()        # Request ACK to sended MSG
    uavcom.synchronize()    # Syncronize the NRX Table

    while 1:
        if uavcom.radio.isRadioAlive()==False : break 
        if ctrl.isAlive == False : break
        uavcom.txCMD(channels=ctrl.getAxis(),force=True)
        time.sleep(0.02)
        # value = uavcom.GET("quad.throttle")
        # print(value)

    ctrl.destroy()
    uavcom.destroy()
    radioManager.closeAvailableRadios()
    
    print("rc commander exit")
    time.sleep(0.1)
    sys.exit()
