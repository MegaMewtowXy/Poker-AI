import random
import socket
import string
import threading
from network.protocol import NetworkProtocol

class RoomServer:
    """
    Multi-Client TCP Socket Server for Texas Hold'em Room-Code Multiplayer.
    Generates 6-character room codes (e.g. PKR-88A2) and broadcasts game state.
    """

    def __init__(self, host="0.0.0.0", port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False
        self.rooms = {}  # room_code -> room_dict
        self.lock = threading.Lock()
        self.thread = None

    @staticmethod
    def ip_to_room_code(ip_address: str) -> str:
        """
        Securely encodes IPv4 address into a clean Room Code (e.g. 192.168.1.15 -> PKR-C0A8010F).
        """
        try:
            parts = [int(p) for p in ip_address.split(".")]
            if len(parts) == 4:
                hex_str = "".join(f"{p:02X}" for p in parts)
                return f"PKR-{hex_str}"
        except Exception:
            pass
        return "PKR-7F000001"

    @staticmethod
    def room_code_to_ip(room_code: str) -> str:
        """
        Decodes Room Code back to target IPv4 address (e.g. PKR-C0A8010F -> 192.168.1.15).
        """
        clean = str(room_code).upper().replace("PKR-", "").replace("-", "").strip()
        if clean == "LOCAL":
            return "127.0.0.1"
        if len(clean) == 8:
            try:
                parts = [str(int(clean[i:i+2], 16)) for i in range(0, 8, 2)]
                return ".".join(parts)
            except Exception:
                pass
        return "127.0.0.1"

    def generate_room_code(self):
        return self.ip_to_room_code(self.get_local_ip())

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def start(self):
        if self.is_running:
            return
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.is_running = True

        self.thread = threading.Thread(target=self._accept_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass

    def _accept_loop(self):
        while self.is_running:
            try:
                client_sock, addr = self.server_socket.accept()
                threading.Thread(target=self._client_handler, args=(client_sock, addr), daemon=True).start()
            except Exception:
                break

    def _client_handler(self, client_sock, addr):
        buffer = bytearray()
        client_room_code = None
        player_name = None

        try:
            while self.is_running:
                data = client_sock.recv(4096)
                if not data:
                    break
                buffer.extend(data)
                packets = NetworkProtocol.decode_stream(buffer)

                for pkt in packets:
                    p_type = pkt.get("type")
                    p_data = pkt.get("data", {})

                    if p_type == NetworkProtocol.CREATE_ROOM:
                        with self.lock:
                            room_code = self.generate_room_code()
                            player_name = p_data.get("host_name", "Host")
                            self.rooms[room_code] = {
                                "code": room_code,
                                "host_sock": client_sock,
                                "host_name": player_name,
                                "starting_chips": p_data.get("starting_chips", 1000),
                                "small_blind": p_data.get("small_blind", 10),
                                "big_blind": p_data.get("big_blind", 20),
                                "clients": [(client_sock, player_name)],
                                "game_started": False
                            }
                            client_room_code = room_code

                        # Send response back to host
                        resp = NetworkProtocol.encode(NetworkProtocol.ROOM_STATE, {
                            "room_code": room_code,
                            "is_host": True,
                            "players": [player_name],
                            "starting_chips": p_data.get("starting_chips", 1000),
                            "small_blind": p_data.get("small_blind", 10),
                            "big_blind": p_data.get("big_blind", 20)
                        })
                        client_sock.sendall(resp)

                    elif p_type == NetworkProtocol.JOIN_ROOM:
                        requested_code = p_data.get("room_code", "").upper()
                        player_name = p_data.get("player_name", "Player")

                        with self.lock:
                            room = self.rooms.get(requested_code)
                            if not room:
                                err = NetworkProtocol.encode(NetworkProtocol.ERROR, {"message": f"Room '{requested_code}' not found!"})
                                client_sock.sendall(err)
                                continue

                            if len(room["clients"]) >= 9:
                                err = NetworkProtocol.encode(NetworkProtocol.ERROR, {"message": "Room is full! (Max 9 players)"})
                                client_sock.sendall(err)
                                continue

                            room["clients"].append((client_sock, player_name))
                            client_room_code = requested_code

                            # Broadcast updated room state to all room clients
                            player_list = [name for _, name in room["clients"]]
                            state_pkt = NetworkProtocol.encode(NetworkProtocol.ROOM_STATE, {
                                "room_code": requested_code,
                                "players": player_list,
                                "starting_chips": room["starting_chips"],
                                "small_blind": room["small_blind"],
                                "big_blind": room["big_blind"]
                            })

                            for sock, _ in room["clients"]:
                                try: sock.sendall(state_pkt)
                                except Exception: pass

                    elif p_type in (NetworkProtocol.START_GAME, NetworkProtocol.GAME_ACTION, NetworkProtocol.STATE_SYNC):
                        if client_room_code and client_room_code in self.rooms:
                            room = self.rooms[client_room_code]
                            broadcast_pkt = NetworkProtocol.encode(p_type, p_data)
                            for sock, _ in room["clients"]:
                                if sock != client_sock:
                                    try: sock.sendall(broadcast_pkt)
                                    except Exception: pass
        except Exception:
            pass
        finally:
            client_sock.close()
