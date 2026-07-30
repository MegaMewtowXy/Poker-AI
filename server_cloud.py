import os
import sys
import time

# Ensure project root is in import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from network.server import RoomServer

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9999))
    print(f"Starting Texas Hold'em Free Cloud Relay Server on port {port}...")
    server = RoomServer(host="0.0.0.0", port=port)
    server.start()
    
    print(f"Cloud Relay Server is online on port {port}! Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping Cloud Relay Server...")
        server.stop()
