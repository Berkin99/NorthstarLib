import sys
sys.path.append('./')

import northlib.ncmd.nrx as nrx


el = nrx.NRX_INT16

tel = nrx.NrxType(el)

print("vartype: ", tel.varType)
print("varbytes:", tel.varBytes)
print("readonly:", tel.readOnly)
print("group:   ", tel.group)
