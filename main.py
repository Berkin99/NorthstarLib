
import northlib

from northlib.ntrp import northbuffer

nc = northbuffer.NorthBuffer(4)

nc.append("ER")
nc.append("ERR")
nc.append("ERRR")
