#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

"""
Background daemon for managing UAV connections
Handles multiple client requests and maintains UAV connections
"""

import json
import socket
import threading
import time
from ncconfig import NorthConfig

__author__ = 'Yeniay RD'
__all__ = ['NorthDaemon']


class NorthDaemon:
    """North Daemon for managing UAV connections"""
    
    def __init__(self):
        self.config = NorthConfig()
        self.uav_connections = {}
        self.running = False
        self.server_socket = None
    
    def _init_radios(self):
        """Initialize radio connections"""
        try:
            import sys
            from pathlib import Path
            # Add parent directory to path to find northlib
            parent_dir = str(Path(__file__).parent.parent)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            
            from northlib import ntrp as radio_manager
            radio_manager.radioSearch(baud=2000000)
            if not radio_manager.getAvailableRadios():
                print("Warning: No radios found")
            return True
        except ImportError:
            print("Error: Cannot import northlib. Check installation.")
            return False
        except Exception as e:
            print(f"Error initializing radios: {e}")
            return False
    
    def _connect_linked_agents(self):
        """Connect to all linked agents"""
        try:
            import sys
            from pathlib import Path
            # Add parent directory to path to find northswarm
            parent_dir = str(Path(__file__).parent.parent)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            
            from northswarm.uavcom import UavCOM
            
            linked_agents = self.config.load_links()
            for agent_id in linked_agents:
                uri = f"radio:/0/76/2/E7E7E7E{int(agent_id):03d}"
                com = UavCOM(uri)
                com.start()
                self.uav_connections[agent_id] = com
                time.sleep(0.05)  # Small delay between connections
        except ImportError:
            print("Error: Cannot import northswarm. Check installation.")
        except Exception as e:
            print(f"Error connecting to agents: {e}")
    
    def _handle_client(self, client_socket):
        """Handle individual client request"""
        try:
            # Receive request
            request_data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                request_data += chunk
            
            if not request_data:
                return
            
            request = json.loads(request_data.decode('utf-8'))
            response = self._process_request(request)
            
            # Send response
            response_data = json.dumps(response).encode('utf-8')
            client_socket.sendall(response_data)
            
        except Exception as e:
            print(f"Error handling client: {e}")
            error_response = {"ok": False, "error": str(e)}
            try:
                client_socket.sendall(json.dumps(error_response).encode('utf-8'))
            except:
                pass
        finally:
            client_socket.close()
    
    def _process_request(self, request):
        """Process incoming request and return response"""
        action = request.get("action")
        
        if action == "link":
            return self._handle_link(request)
        elif action == "unlink":
            return self._handle_unlink(request)
        elif action == "status":
            return self._handle_status(request)
        elif action == "cmd":
            return self._handle_command(request)
        elif action == "shutdown":
            return self._handle_shutdown()
        else:
            return {"ok": False, "error": f"Unknown action: {action}"}
    
    def _handle_link(self, request):
        """Handle agent linking request"""
        try:
            new_ids = request.get("ids", [])
            current_ids = self.config.load_links()
            all_ids = list(set(current_ids + new_ids))
            self.config.save_links(all_ids)
            
            # Try to connect new agents
            for agent_id in new_ids:
                if agent_id not in self.uav_connections:
                    try:
                        import sys
                        from pathlib import Path
                        # Add parent directory to path to find northswarm
                        parent_dir = str(Path(__file__).parent.parent)
                        if parent_dir not in sys.path:
                            sys.path.insert(0, parent_dir)
                        
                        from northswarm.uavcom import UavCOM
                        uri = f"radio:/0/76/2/E7E7E7E{int(agent_id):03d}"
                        com = UavCOM(uri)
                        com.start()
                        self.uav_connections[agent_id] = com
                        time.sleep(0.05)
                    except Exception as e:
                        print(f"Failed to connect agent {agent_id}: {e}")
            
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def _handle_unlink(self, request):
        """Handle agent unlinking request"""
        try:
            if request.get("all", False):
                self.config.save_links([])
                # Disconnect all agents
                for agent_id, com in list(self.uav_connections.items()):
                    try:
                        com.close()
                    except:
                        pass
                self.uav_connections.clear()
            else:
                ids_to_remove = request.get("ids", [])
                current_ids = self.config.load_links()
                remaining_ids = [id for id in current_ids if id not in ids_to_remove]
                self.config.save_links(remaining_ids)
                
                # Disconnect specified agents
                for agent_id in ids_to_remove:
                    if agent_id in self.uav_connections:
                        try:
                            self.uav_connections[agent_id].close()
                            del self.uav_connections[agent_id]
                        except:
                            pass
            
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def _handle_status(self, request):
        """Handle status request"""
        try:
            target_ids = request.get("ids")
            if target_ids is None:
                target_ids = self.config.load_links()
            
            status_info = {}
            for agent_id in target_ids:
                if agent_id in self.uav_connections:
                    com = self.uav_connections[agent_id]
                    agent_status = {}
                    
                    try:
                        if request.get("pos", False):
                            agent_status["pos"] = com.getPosition()
                        if request.get("rot", False):
                            agent_status["rot"] = com.getRotation()
                        if request.get("nav", False):
                            agent_status["nav"] = com.getNavigation()
                        if request.get("batt", False):
                            agent_status["batt"] = com.getBattery()
                    except Exception as e:
                        agent_status["error"] = f"Communication error: {e}"
                    
                    status_info[agent_id] = agent_status
                else:
                    status_info[agent_id] = {"error": "Not connected"}
            
            return {"ok": True, "status": status_info}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def _handle_command(self, request):
        """Handle command request"""
        try:
            agent_id = request.get("id")
            if agent_id not in self.uav_connections:
                return {"ok": False, "error": f"Agent {agent_id} not connected"}
            
            com = self.uav_connections[agent_id]
            
            if request.get("takeoff", False):
                com.takeOff()
            elif request.get("land", False):
                com.land()
            elif request.get("pos"):
                pos = request["pos"]
                com.setPosition(pos[0], pos[1], pos[2])
            else:
                return {"ok": False, "error": "No valid command specified"}
            
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def _handle_shutdown(self):
        """Handle shutdown request"""
        print("Shutdown requested")
        self.running = False
        return {"ok": True}
    
    def run(self, host="127.0.0.1", port=7777):
        """Start the daemon"""
        print(f"Starting North Daemon on {host}:{port}")
        
        # Initialize radios
        if not self._init_radios():
            print("Failed to initialize radios. Continuing anyway...")
        
        # Save daemon info
        self.config.save_daemon_info(host, port)
        
        # Connect to linked agents
        self._connect_linked_agents()
        print(f"Connected to {len(self.uav_connections)} agents")
        
        # Start server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            self.running = True
            
            print("Daemon ready. Press Ctrl+C to stop.")
            
            while self.running:
                try:
                    self.server_socket.settimeout(1.0)
                    client_socket, addr = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self._handle_client, 
                        args=(client_socket,),
                        daemon=True
                    )
                    client_thread.start()
                except socket.timeout:
                    continue
                except OSError:
                    if self.running:
                        print("Server socket error")
                    break
                    
        except Exception as e:
            print(f"Error running daemon: {e}")
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Clean up resources"""
        print("Shutting down daemon...")
        
        # Close all UAV connections
        for com in self.uav_connections.values():
            try:
                com.close()
            except:
                pass
        self.uav_connections.clear()
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        # Remove daemon info file
        self.config.remove_daemon_info()
        
        print("Daemon stopped")