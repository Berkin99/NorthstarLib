# Northstar Library

NorthstarLib provides a collection of tools for communicating with UAVs and other
embedded agents over a custom lightweight protocol called **NTRP** (Northstar
Radio Protocol).  The project contains both the Python implementation used on
the computer side as well as example firmware for a radio "dongle" that bridges
USB and RF modules.

## Repository layout

- **`northlib/`** – Python packages that implement the protocol and high level
  controllers
  - **`ntrp`** – low level protocol definitions and radio utilities
  - **`ncmd`** – the command/response layer for controlling agents
- **`northdongle/`** – Arduino examples that turn a microcontroller into a
  radio router for NTRP
- **`northswarm/`** – experimental UAV control utilities built on top of
  northlib
- **`examples/`** – small example programs showing how to use the API

## Key concepts

`northlib` exposes a few core classes:

- **`NorthPort`** – wraps a serial port and handles safe access
- **`NorthRadio`** – manages communication with the radio dongle. It keeps a
  list of **`NorthPipe`** objects, each representing a connection to a single
  agent.
- **`NorthPipe`** – sends and receives NTRP packets for one agent. Messages can
  be buffered or handled via callbacks.
- **`NTRPMessage` / `NTRPPacket`** – container classes used to build and parse
  protocol frames.

Agents are addressed using short identifiers (pipe IDs).  The radio assigns a
new ID using `newPipeID()` whenever a pipe is created.  Each pipe can then send
commands (GET, SET, RUN, LOG, etc.) or arbitrary data to the agent.

## Building the dongle firmware

The `northdongle/arduinorouter` directory contains a minimal firmware
implementation of the protocol in C++ that can run on an Arduino compatible
board equipped with an NRF24 or similar RF module.  Open the `.ino` project in
Arduino IDE and flash it to the board.  Once programmed, the dongle exposes a
USB serial interface that can be used with the Python API.

## Python usage

Clone this repository and install the required dependencies:

```bash
pip install pyserial
```

The examples rely on a radio dongle being connected and exposed as a serial
port.  To search for connected radios:

```python
import northlib.ntrp as radioManager
radioManager.radioSearch(baud=115200)
print(radioManager.availableRadios)
```

Opening a pipe and sending commands:

```python
from northlib.ntrp.northpipe import NorthPipe

radio = radioManager.availableRadios[0]
pipe = NorthPipe(pipe_id=radio.newPipeID(), radio=radio)
pipe.setRxHandleMode(NorthPipe.RX_HANDLE_MODE_CALLBACK)
pipe.setCallBack(ntrp.NTRPHeader_e.MSG, lambda msg: print(msg.data))
pipe.txGET(1)  # request parameter 1
```

See the scripts inside the `examples/` directory for more complete usage
patterns such as UAV control and live plotting of telemetry.

## Development notes

Two small but important fixes were recently applied:

1. **`NTRPMessage.setPacket`** now correctly copies the data ID from the source
   packet.
2. **`NorthRadio.newPipeID`** returns a sequential identifier instead of
   reusing the highest existing one.

After modifying the library run the basic syntax check:

```bash
python -m py_compile northlib/ntrp/ntrp.py northlib/ntrp/northradio.py
find northlib -name '*.py' | xargs python -m py_compile
```

## License

This project is released under the GNU General Public License version 3.  See
individual source files for detailed copyright headers.
