import queue
import socket
import threading
from network.protocol import NetworkProtocol

class NetworkClient:
    """
    Non-Blocking Pygame Network Client for Room-Code Multiplayer.
    Listens on a background daemon thread and enqueues events for the main Pygame loop.
    """

    CLOUD_SERVER_HOST = "poker-ai-c4ar.onrender.com"

    def __init__(self):
        self.sock = None
        self.is_connected = False
        self.thread = None
        self.event_queue = queue.Queue()
        self.current_room_code = None
        self.is_host = False

    def connect(self, host=None, port=9999):
        if host is None:
            host = self.CLOUD_SERVER_HOST
        try:
            target_ip = socket.gethostbyname(host)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((target_ip, port))
            self.is_connected = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            return True
        except Exception:
            self.is_connected = False
            return False

    def disconnect(self):
        self.is_connected = False
        if self.sock:
            try: self.sock.close()
            except Exception: pass

    def send(self, msg_type: str, data: dict = None):
        if self.is_connected and self.sock:
            try:
                pkt = NetworkProtocol.encode(msg_type, data)
                self.sock.sendall(pkt)
            except Exception:
                self.is_connected = False

    def _listen_loop(self):
        buffer = bytearray()
        while self.is_connected:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                buffer.extend(data)
                packets = NetworkProtocol.decode_stream(buffer)
                for pkt in packets:
                    self.event_queue.put(pkt)
            except Exception:
                break
        self.is_connected = False

    def poll_events(self):
        events = []
        while not self.event_queue.empty():
            try:
                events.append(self.event_queue.get_nowait())
            except queue.Empty:
                break
        return events
