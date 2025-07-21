#!/usr/bin/env python3
"""
NorthstarLib CLI - Main Entry Point
Simple command-line interface for UAV management
"""

import argparse
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ncclient import NorthClient
from ncconfig import NorthConfig


def handle_link(args):
    """Link agents to the daemon"""
    try:
        client = NorthClient()
        response = client.send_request({
            "action": "link", 
            "ids": [str(x) for x in args.ids]
        })
        
        if response and response.get("ok"):
            for agent_id in args.ids:
                print(f"Linked agent {agent_id}")
        else:
            print("Failed to link agents")
            
    except Exception as e:
        print(f"Error: {e}")


def handle_unlink(args):
    """Unlink agents from the daemon"""
    try:
        client = NorthClient()
        response = client.send_request({
            "action": "unlink",
            "ids": [str(x) for x in args.ids] if not args.all else [],
            "all": args.all
        })
        
        if response and response.get("ok"):
            if args.all:
                print("All agents unlinked")
            else:
                for agent_id in args.ids:
                    print(f"Unlinked agent {agent_id}")
        else:
            print("Failed to unlink agents")
            
    except Exception as e:
        print(f"Error: {e}")


def handle_status(args):
    """Get status from agents"""
    try:
        client = NorthClient()
        response = client.send_request({
            "action": "status",
            "ids": [str(x) for x in args.ids] if args.ids else None,
            "pos": args.pos,
            "rot": args.rot,
            "nav": args.nav,
            "batt": args.batt
        })
        
        if response and "status" in response:
            for agent_id, info in response["status"].items():
                print(f"Agent {agent_id}:")
                if "error" in info:
                    print(f"  Error: {info['error']}")
                    continue
                    
                if args.pos and "pos" in info:
                    print(f"  Position: {info['pos']}")
                if args.rot and "rot" in info:
                    print(f"  Rotation: {info['rot']}")
                if args.nav and "nav" in info:
                    print(f"  Navigation: {info['nav']}")
                if args.batt and "batt" in info:
                    print(f"  Battery: {info['batt']}")
        else:
            print("Failed to get status")
            
    except Exception as e:
        print(f"Error: {e}")


def handle_cmd(args):
    """Send commands to agents"""
    try:
        client = NorthClient()
        response = client.send_request({
            "action": "cmd",
            "id": str(args.id),
            "takeoff": args.takeoff,
            "land": args.land,
            "pos": args.pos
        })
        
        if response and response.get("ok"):
            cmd_name = "takeoff" if args.takeoff else "land" if args.land else f"position {args.pos}"
            print(f"Command '{cmd_name}' sent to agent {args.id}")
        else:
            print("Failed to send command")
            
    except Exception as e:
        print(f"Error: {e}")


def handle_run(args):
    """Start the daemon"""
    try:
        from ncdaemon import NorthDaemon
        daemon = NorthDaemon()
        daemon.run(host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("Daemon stopped")
    except Exception as e:
        print(f"Error starting daemon: {e}")


def handle_stop(args):
    """Stop the daemon"""
    try:
        client = NorthClient()
        response = client.send_request({"action": "shutdown"})
        if response:
            print("Daemon stopped")
        else:
            print("Could not stop daemon (may not be running)")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(prog="nc", description="NorthstarLib CLI")
    subparsers = parser.add_subparsers(dest="cmd")

    # Link command
    link_parser = subparsers.add_parser("link", help="Link agents")
    link_parser.add_argument("ids", nargs="+", type=int, help="Agent IDs")
    link_parser.set_defaults(func=handle_link)

    # Unlink command
    unlink_parser = subparsers.add_parser("unlink", help="Unlink agents")
    unlink_parser.add_argument("ids", nargs="*", type=int, help="Agent IDs")
    unlink_parser.add_argument("--all", action="store_true", help="Unlink all")
    unlink_parser.set_defaults(func=handle_unlink)

    # Status command
    status_parser = subparsers.add_parser("status", help="Get agent status")
    status_parser.add_argument("ids", nargs="*", type=int, help="Agent IDs")
    status_parser.add_argument("-pos", action="store_true", help="Show position")
    status_parser.add_argument("-rot", action="store_true", help="Show rotation") 
    status_parser.add_argument("-nav", action="store_true", help="Show navigation")
    status_parser.add_argument("-batt", action="store_true", help="Show battery")
    status_parser.set_defaults(func=handle_status)

    # Command
    cmd_parser = subparsers.add_parser("cmd", help="Send commands")
    cmd_parser.add_argument("id", type=int, help="Agent ID")
    cmd_group = cmd_parser.add_mutually_exclusive_group(required=True)
    cmd_group.add_argument("-takeoff", action="store_true", help="Take off")
    cmd_group.add_argument("-land", action="store_true", help="Land")
    cmd_group.add_argument("-pos", nargs=3, type=float, help="Set position X Y Z")
    cmd_parser.set_defaults(func=handle_cmd)

    # Daemon commands
    run_parser = subparsers.add_parser("run", help="Start daemon")
    run_parser.add_argument("--host", default="127.0.0.1", help="Host address")
    run_parser.add_argument("--port", type=int, default=7777, help="Port number")
    run_parser.set_defaults(func=handle_run)

    stop_parser = subparsers.add_parser("stop", help="Stop daemon")
    stop_parser.set_defaults(func=handle_stop)

    # Parse and execute
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()