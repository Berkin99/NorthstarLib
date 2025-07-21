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
Client communication module
Handles sending requests to the daemon
"""

import json
import socket
from ncconfig import NorthConfig

__author__ = 'Yeniay RD'
__all__ = ['NorthClient']


class NorthClient:
    """North Client for communicating with NorthDaemon"""
    
    def __init__(self):
        self.config = NorthConfig()
    
    def send_request(self, request):
        """Send request to daemon and get response"""
        host, port = self.config.load_daemon_info()
        
        try:
            # Connect to daemon
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            # Send request
            request_data = json.dumps(request).encode('utf-8')
            sock.sendall(request_data)
            sock.shutdown(socket.SHUT_WR)
            
            # Get response
            response_data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            
            sock.close()
            
            if response_data:
                return json.loads(response_data.decode('utf-8'))
                
        except socket.timeout:
            raise Exception("Daemon not responding (timeout)")
        except ConnectionRefusedError:
            raise Exception("Could not connect to daemon. Is it running?")
        except Exception as e:
            raise Exception(f"Communication error: {e}")
        
        return None