#!/usr/bin/env python3
"""NorthstarLib Command Line Interface

This tool provides a small helper around the northlib/northswarm
packages to quickly send commands to UAV agents from the terminal.

The command layout tries to mimic the examples given in the project
README and lets you link agents, query their status and issue flight
commands.
"""

import argparse
import json
import os
import sys
import time
import socket

# Import library components. They may fail if dependencies are missing
# but we keep imports local to functions so the CLI can still show help.

LINK_FILE = os.path.expanduser("~/.northstar_links")
DEFAULT_BAUD = 2000000
SOCKET_FILE = os.path.expanduser("~/.northstar_socket")

# Use a UNIX socket if supported, otherwise fall back to a local TCP port so the
# tool can run on Windows as well.
USE_UNIX = hasattr(socket, "AF_UNIX")
SOCKET_ADDR = SOCKET_FILE if USE_UNIX else ("127.0.0.1", 28600)


def load_links():
    if not os.path.exists(LINK_FILE):
        return []
    try:
        with open(LINK_FILE, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return []


def save_links(ids):
    with open(LINK_FILE, "w", encoding="utf-8") as fp:
        json.dump(ids, fp)


def send_request(req):
    if USE_UNIX and not os.path.exists(SOCKET_FILE):
        print("Daemon not running. Start it with 'nc run'", file=sys.stderr)
        return None
    try:
        s = socket.socket(socket.AF_UNIX if USE_UNIX else socket.AF_INET,
                          socket.SOCK_STREAM)
        s.connect(SOCKET_ADDR)
        s.sendall(json.dumps(req).encode())
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        s.close()
        if data:
            return json.loads(data.decode())
    except Exception as exc:
        print(f"Communication error: {exc}", file=sys.stderr)
    return None


def uri_from_id(uav_id, radio_index=0):
    return f"radio:/{radio_index}/76/2/E7E7E7E{int(uav_id):03d}"


def connect(ids):
    """Initialise radios and create UavCOM objects for given ids."""
    from northlib import ntrp as radioManager
    from northswarm.uavcom import UavCOM

    radioManager.radioSearch(baud=DEFAULT_BAUD)
    if not radioManager.getAvailableRadios():
        print("No radios found", file=sys.stderr)
        return {}

    connections = {}
    for i, uid in enumerate(ids):
        uri = uri_from_id(uid)
        com = UavCOM(uri)
        com.start()
        connections[uid] = com
        # small delay to avoid flooding the radio initialisation
        time.sleep(0.05)
    return connections


def close(connections):
    from northlib import ntrp as radioManager

    for com in connections.values():
        com.destroy()
    radioManager.closeAvailableRadios()


def server_loop():
    from northswarm.uavcom import UavCOM
    coms = {}
    ids = load_links()
    if ids:
        coms = connect(ids)

    if USE_UNIX and os.path.exists(SOCKET_FILE):
        os.remove(SOCKET_FILE)

    sock = socket.socket(socket.AF_UNIX if USE_UNIX else socket.AF_INET,
                         socket.SOCK_STREAM)
    sock.bind(SOCKET_ADDR)
    sock.listen(1)

    try:
        while True:
            conn, _ = sock.accept()
            data = conn.recv(4096)
            if not data:
                conn.close()
                continue
            req = json.loads(data.decode())
            action = req.get("action")
            resp = {"ok": True}

            if action == "status":
                resp["status"] = {}
                ids_req = req.get("ids") or list(coms.keys())
                for uid in ids_req:
                    com = coms.get(uid)
                    if not com:
                        continue
                    info = {}
                    if req.get("pos"):
                        info["pos"] = com.position
                    if req.get("rot"):
                        info["rot"] = com.heading
                    if req.get("nav"):
                        info["nav"] = com.rc
                    if req.get("batt"):
                        try:
                            info["batt"] = com.GET("battery")
                        except Exception:
                            info["batt"] = "unknown"
                    resp["status"][uid] = info

            elif action == "cmd":
                uid = req.get("id")
                com = coms.get(uid)
                if com:
                    if req.get("takeoff"):
                        cmd_takeoff(com)
                    elif req.get("land"):
                        cmd_land(com)
                    elif req.get("pos") is not None:
                        cmd_pos(com, req.get("pos"))

            elif action == "link":
                ids_new = [str(i) for i in req.get("ids", [])]
                links = set(load_links())
                links.update(ids_new)
                save_links(sorted(links))
                for uid in ids_new:
                    if uid not in coms:
                        com = UavCOM(uri_from_id(uid))
                        com.start()
                        coms[uid] = com

            elif action == "unlink":
                if req.get("all"):
                    save_links([])
                    for com in coms.values():
                        com.destroy()
                    coms = {}
                else:
                    ids_del = [str(i) for i in req.get("ids", [])]
                    links = set(load_links())
                    for uid in ids_del:
                        links.discard(uid)
                        if uid in coms:
                            coms[uid].destroy()
                            del coms[uid]
                    save_links(sorted(links))

            elif action == "shutdown":
                resp["msg"] = "shutdown"
                conn.sendall(json.dumps(resp).encode())
                conn.close()
                break

            conn.sendall(json.dumps(resp).encode())
            conn.close()
    finally:
        if USE_UNIX and os.path.exists(SOCKET_FILE):
            os.remove(SOCKET_FILE)
        close(coms)


def cmd_takeoff(com):
    com.takeOff()


def cmd_land(com):
    com.land()


def cmd_pos(com, pos):
    com.setPosition(pos)
    com.setAuto()


def handle_link(args):
    req = {"action": "link", "ids": [str(x) for x in args.ids]}
    resp = send_request(req)
    if resp:
        for uid in args.ids:
            print(f"Linked {uid}")


def handle_unlink(args):
    req = {"action": "unlink", "ids": [str(x) for x in args.ids], "all": args.all}
    resp = send_request(req)
    if resp:
        if args.all:
            print("All links cleared")
        else:
            for uid in args.ids:
                print(f"Unlinked {uid}")


def handle_status(args):
    req = {
        "action": "status",
        "ids": [str(x) for x in args.ids] if args.ids else None,
        "pos": args.pos,
        "rot": args.rot,
        "nav": args.nav,
        "batt": args.batt,
    }
    resp = send_request(req)
    if resp and "status" in resp:
        for uid, info in resp["status"].items():
            print(f"Status {uid}:")
            if args.pos and "pos" in info:
                print("pos", info["pos"])
            if args.rot and "rot" in info:
                print("rot", info["rot"])
            if args.nav and "nav" in info:
                print("nav", info["nav"])
            if args.batt and "batt" in info:
                print("batt", info["batt"])


def handle_cmd(args):
    req = {
        "action": "cmd",
        "id": str(args.id),
        "takeoff": args.takeoff,
        "land": args.land,
        "pos": args.pos,
    }
    send_request(req)


def handle_run(args):
    print("Daemon running. Linked agents:", ", ".join(load_links()))
    server_loop()


def handle_stop(args):
    req = {"action": "shutdown"}
    send_request(req)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="nc", description="Northstar CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_status = sub.add_parser("status", help="show agent status")
    p_status.add_argument("ids", nargs="*", help="agent ids")
    p_status.add_argument("-pos", action="store_true", dest="pos")
    p_status.add_argument("-rot", action="store_true", dest="rot")
    p_status.add_argument("-nav", action="store_true", dest="nav")
    p_status.add_argument("-batt", action="store_true", dest="batt")
    p_status.set_defaults(func=handle_status)

    p_link = sub.add_parser("link", help="remember agents")
    p_link.add_argument("ids", nargs="+")
    p_link.set_defaults(func=handle_link)

    p_unlink = sub.add_parser("unlink", help="forget agents")
    p_unlink.add_argument("ids", nargs="*")
    p_unlink.add_argument("--all", action="store_true", dest="all")
    p_unlink.set_defaults(func=handle_unlink)

    p_cmd = sub.add_parser("cmd", help="send flight commands")
    p_cmd.add_argument("id")
    g = p_cmd.add_mutually_exclusive_group(required=True)
    g.add_argument("-takeoff", action="store_true", dest="takeoff")
    g.add_argument("-land", action="store_true", dest="land")
    g.add_argument("-pos", nargs=3, type=float, dest="pos")
    p_cmd.set_defaults(func=handle_cmd)

    p_run = sub.add_parser("run", help="start background daemon")
    p_run.set_defaults(func=handle_run)

    p_stop = sub.add_parser("stop", help="stop daemon")
    p_stop.set_defaults(func=handle_stop)

    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
