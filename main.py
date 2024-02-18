
import northlib.ntrp
from northlib.ntrp import RadioManager
from northlib.ntrp.northport import NorthPort

from enum import Enum

import time

if __name__ == '__main__':

    print("OK".encode())
    rmg = RadioManager()
    rmg.radioSearch()
    time.sleep(2)
    rmg.radioClose()
