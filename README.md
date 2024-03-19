
# Northstar 0.2

### Northstar Radio Protocol (NTRP)

Northstar radio protocol is optimised low level communication & debugging.
This protocol aimed to comminicate with target computer like a debugger.
Interactions (Get, Set, Run headers) happen with tags. Tag represents variable
or function address.

#### Example 
#### NTRP Package : |Header(1b)|DataId(1b)|Data(xb)|
#### NTRP Message : |'*'|TalkerID|ReceiverID|PackageLen|<NTRP_Package>|'\n'|

#### Header:
> Get variable 
> Set variable  
> Run function 
> Log request 
> Specializable Commands
> Carry debug messages

### Northradio

Northradio handles the communication. Receives all NTRP messages and routes
to the related NorthPipe. NorthPipe stores the NTRP_Messages. 