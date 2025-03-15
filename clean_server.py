"""Clean up server processes and sockets"""
import psutil
import os
import sys
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if hasattr(conn.laddr, 'port') and conn.laddr.port == port:
                    logger.info(f"Killing process {proc.pid} using port {port}")
                    proc.kill()
                    proc.wait()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            continue

def cleanup_server(port=8000):
    """Full server cleanup routine"""
    # Kill any processes using our port
    kill_process_on_port(port)
    
    # Clean up any stale .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
        for dir in dirs:
            if dir == '__pycache__':
                os.rmdir(os.path.join(root, dir))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    cleanup_server(port)