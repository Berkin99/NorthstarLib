import sys
sys.path.append('./')

import sys
import time

import northlib.ntrp as radioManager
from northlib.ncmd.northcom import NorthCOM
from northlib.ncmd.nrxtable import NrxTableLog

uri = "radio:/0/76/2/E7E7E7E301"

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000) #Arduino DUE (USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()
    
    time.sleep(1)
    
    uavcom = NorthCOM(uri=uri)
    uavcom.connect()
    uavcom.synchronize()
    
    time.sleep(1)
    
    vector = uavcom.GET("vector")
    print(vector)

    uavcom.SET("vector",[31,62,93])
    time.sleep(1)
    
    vector = uavcom.GET("vector")
    print(vector)
    
    nx = uavcom.paramtable.search("vector")

    while uavcom.radio.isRadioAlive():
        uavcom.txGET(nx.index)
        NrxTableLog(uavcom.paramtable)
        time.sleep(1)
    
    uavcom.destroy()
    radioManager.closeAvailableRadios()
    sys.exit()
