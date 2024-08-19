
# **NORTHLIB API**

**Northlib** is a wireless communication protocol supervisor for communicating 
external embedded devices with PC.

#### System Elements: 
* Command Station : Northlib worker, Computer (PC) 
* Dongle : Radio Transreceiver connected to PC via USB
* Agent  : Target embedded device that we aim to communicate
* NTRP   : Northstar Radio Protocol, communication protocol
* NCMD   : Northstar Commander, command operator.
* Pipe   : Virtual comminication line between agent and related ntrp object

#### Northlib Communication Services:
* Real time data monitoring
* Real time data updating
* Function call in the embedded device
* Multi agent operations
* 2mbps comminication speed

## NTRP

NTRP is a sublib for provide  Northstar Radio Protocol.  The protocol is  a 
double sided agreement between agent and commander. It presents the meaning
and metadata of the data that received/transmitted.

Northstar  radio  protocol is optimised low level communication & debugging.
This protocol  aimed  to comminicate with target computer like  a  debugger.
Interactions  (Get, Set, Run ... headers) happen with tags.   Tag represents 
variable or function address.

[NTRP] sublibrary classes:

* NTRP
    * **NTRPPacket**  : Northstar Radio Protocol Packet type Payload
    * **NTRPMessage** : Northstar Radio Protocol Message type Payload.
* NorthPort : Serial communication provider 
* NorthRadio(NorthPort) : Telemetry Dongle Proxy 
* NorthPipe : Opened router pipes under NorthRadio.  Communicate  multiple
agents with single radio. It can use with LORA or NRF types of dongle 
* NorthNRF(NorthPipe) : NRF type dongle Pipe 

### NTRP/NTRP 

There is two types of payload. NTRP Package and the helper wrapped version 
of package as NTRP Message.

* NTRP Package : [Header][DataId][Data1][Data2][...][DataN]
* NTRP Message : ['*'][TalkerID][ReceiverID][PackageLen][<NTRP_Package>]['\n']

#### Header:
* Get variable 
* Set variable  
* Run function 
* Log request 
* Specializable Commands
* Carry debug messages

### NTRP/NorthPort
Northport is a Serial COM wrapper. It uses pyserial for general usb applications
Can be customized for different types of PC-Dongle communication applications.

### NTRP/NorthRadio
Proxy of connected RF Dongle.

Northradio Services: 
* Searches for NRF dongles in the USB ports and sync with it.
* Parses and Routes received **bytearray** data to related pipe as NTRPPacket. 
* Gets NTRPPacket as input and unites to **bytearray** for transmission
* Can be customized for multi Commander applicatons.

### NTRP/NorthPipe

USAGE 1 Dongle(Router) : 
[PC] <--- USB ---> [DONGLE] <--- SPI ---> [RF] <   RF   > [NODE1,NODE2...]

USAGE 2 LORA: 
[PC] <--- USB ---> [USB_TO_UART_CONVERTER] <--- UART ---> [LORA] <  LORA  > [NODE1,NODE2...]


## NCMD