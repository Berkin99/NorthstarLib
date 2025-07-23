# NorthCLI (nc.py)

A simple command-line tool for managing UAV agents using the northlib/northswarm packages.

### NC Daemon 

#### `nc.py run [--host HOST] [--port PORT]`
Start the background daemon that manages UAV connections.

**Options:**
- `--host`: Host address (default: 127.0.0.1)
- `--port`: Port number (default: 7777)

**Examples:**
```bash
python nc.py run                    # Start daemon on default host/port
python nc.py run --port 8888        # Start daemon on port 8888
python nc.py run --host 0.0.0.0     # Listen on all interfaces
```

#### `nc.py stop`
Stop the running daemon.

```bash
python nc.py stop
```

### Agent Management

#### `nc.py link <agent_id> [agent_id2] [agent_id3] ...`
Link agents to the daemon for management. Linked agents will be automatically connected when the daemon starts.

**Examples:**
```bash
python nc.py link 101               # Link single agent
python nc.py link 101 102 103       # Link multiple agents
```

#### `nc.py unlink [agent_id] [agent_id2] ... [--all]`
Unlink agents from the daemon.

**Options:**
- `--all`: Unlink all agents

**Examples:**
```bash
python nc.py unlink 101             # Unlink single agent
python nc.py unlink 101 102         # Unlink multiple agents
python nc.py unlink --all           # Unlink all agents
```

### Status and Monitoring

#### `nc.py status [agent_id] [agent_id2] ... [-pos] [-rot] [-nav] [-batt]`
Get status information from agents.

**Options:**
- `-pos`: Show position data
- `-rot`: Show rotation/heading data
- `-nav`: Show navigation/RC data
- `-batt`: Show battery level

**Examples:**
```bash
python nc.py status                   # Status of all linked agents (basic)
python nc.py status 101               # Status of specific agent
python nc.py status -pos -batt --all  # Position and battery for all agents
python nc.py status 101 102 -pos      # Position for specific agents
```

### Live Commands

#### `nc.py <agent_id> <command>`
Send flight commands to agents.

**Commands:**
- `-arm`: Arm
- `-disarm`: Disarm
- `-takeoff`: Take off
- `-land`: Land
- `-pos X Y Z`: Set position (in meters)

**Examples:**
```bash
python nc.py link 101                 # Connection
python nc.py 101 -takeoff -h="10"     # Take off
python nc.py 101 -land                # Land
python nc.py 101 -pos="10.5,20.0,5.0" # Go to position X=10.5, Y=20.0, Z=5.0
```

## Typical Workflow

1. **Start the daemon:**
   ```bash
   python nc.py run
   ```
   Keep this terminal open. The daemon will show connection status and linked agents.

2. **In another terminal, link your agents:**
   ```bash
   python nc.py link 101 102 103
   ```

3. **Check if they're connected:**
   ```bash
   python nc.py status -batt
   ```

4. **Send some commands:**
   ```bash
   python nc.py cmd 101 -takeoff
   python nc.py cmd 102 -takeoff
   python nc.py cmd 103 -takeoff
   ```

5. **Monitor positions:**
   ```bash
   python nc.py status -pos
   ```

6. **Land them:**
   ```bash
   python nc.py cmd 101 -land
   python nc.py cmd 102 -land
   python nc.py cmd 103 -land
   ```

7. **Stop the daemon when done:**
   ```bash
   python nc.py stop
   ```

## File Structure

The tool consists of 4 simple Python files:

- **`nc.py`** - Main CLI interface
- **`config.py`** - Configuration and file management
- **`client.py`** - Client communication with daemon
- **`daemon.py`** - Background daemon server

## Configuration Files

Configuration files are stored in platform-appropriate locations:

- **Windows**: `%APPDATA%\NorthstarCLI\`
- **macOS/Linux**: `~/.config/northstar/`

Files:
- `links.json` - Linked agent IDs
- `daemon.json` - Daemon connection info (temporary)

## Troubleshooting

### "Could not connect to daemon. Is it running?"
The daemon isn't running. Start it with:
```bash
python nc.py run
```

### "No radios found"
- Check that your radio hardware is connected
- Verify northlib installation
- Check USB permissions (Linux/macOS)

### Agent not responding
- Verify the agent ID is correct
- Check that the agent is powered on
- Try unlinking and linking again:
  ```bash
  python nc.py unlink 101
  python nc.py link 101
  ```

### ImportError for northlib/northswarm
Install the required packages:
```bash
pip install northlib northswarm
```

### Daemon won't start on port
Another process might be using the port. Try a different port:
```bash
python nc.py run --port 8888
```

## Tips

1. **Always start the daemon first** before trying other commands
2. **Link agents once** - they'll reconnect automatically when daemon restarts
3. **Use specific agent IDs** for commands - they're faster than letting the system find them
4. **Check battery levels regularly** with `nc.py status -batt`
5. **Keep the daemon terminal open** to see connection messages and errors