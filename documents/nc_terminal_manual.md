# NC Terminal User Manual

NC Terminal is a command-line interface for controlling UAV agents.  The `nc.py`
script can act both as a daemon that talks to the radios and as a small client
that issues JSON requests to this daemon.  All invocations are done through this
single script.

## Starting NC Terminal

Run the script directly from the repository root.  When executed without any
arguments it prints a help message describing the available subcommands.

```bash
./nc.py -h
```

The most common first step is to start the daemon using the `run` command:

```bash
./nc.py run
```

While the daemon is running it listens for requests from other invocations of
`nc.py`.  On Unix systems a UNIX domain socket `~/.northstar_socket` is used.
On Windows the daemon falls back to TCP port `28600` on `localhost` instead.
Linked agent identifiers are stored in `~/.northstar_links` so that they are
reconnected automatically when the daemon launches.

## Subcommands Overview

* `status` – Query the status of one or more UAVs. Optional flags request specific information:
  * `-pos` – include position data
  * `-rot` – include rotation
  * `-nav` – include RC navigation channels
  * `-batt` – include battery status

* `link` – Remember the given UAV identifiers.  They are written to
  `~/.northstar_links` so the daemon reconnects to them automatically on the next
  launch.

* `unlink` – Remove identifiers from this file.  Use `--all` to forget every
  link and disconnect active connections.

* `cmd` – Send a flight related command to a single UAV. Only one of the following options is allowed per invocation:
  * `-takeoff` – instruct the UAV to take off
  * `-land` – instruct the UAV to land
  * `-pos x y z` – set a target position

* `run` – Launch the NC terminal daemon. This process stays in the foreground and listens for further commands from separate invocations of `nc.py`.

* `stop` – Shut down the daemon if it is running.

## Typical Workflow

1. Start the daemon to communicate with linked UAVs:
   ```bash
   ./nc.py run
   ```
2. In a separate terminal, link agents by their identifiers:
   ```bash
   ./nc.py link 301 302
   ```
3. Send commands to linked UAVs:
   ```bash
   ./nc.py cmd 301 -takeoff
   ./nc.py cmd 301 -pos 0 0 2
   ./nc.py cmd 301 -land
   ```
4. Query status information at any time:
   ```bash
   ./nc.py status -pos -batt
   ```
5. Stop the daemon when finished:
   ```bash
   ./nc.py stop
   ```

NC Terminal expects the radio dongle and its Python dependencies to be available. If no radio is detected, the tool will report an error when trying to connect.

