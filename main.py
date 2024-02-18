
import northlib.ntrp
from northlib.ntrp import RadioManager
from northlib.ntrp.northport import NorthPort

from enum import Enum

import time

if __name__ == '__main__':
    rmg = RadioManager()
    rmg.radioSearch()
    time.sleep(5)
    rmg.radioClose()