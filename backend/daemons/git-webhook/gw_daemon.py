import os
import sys
import socket
import subprocess
from datetime import datetime, timedelta

SOCKET_FILE = 'sockets/git-webhook.sock'
if os.path.exists(SOCKET_FILE):
    os.remove(SOCKET_FILE)

try:
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as server:
        server.bind(SOCKET_FILE)

        while True:
            data = server.recv(128)
            if not data:
                continue
                
            if data != bytearray('\xDE\xAD\xBE\xEF', 'utf-8'):
                continue
                
            date = datetime.now() + timedelta(hours=7)
            date = date.strftime("%d.%m.%Y %H:%M")
            print("\n~~ " + date + " ~~")
            subprocess.Popen(['git', 'pull'])
    
except KeyboardInterrupt:
    os.remove(SOCKET_FILE)


