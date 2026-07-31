import json

class NetworkProtocol:
    """
    JSON Packet Protocol for Texas Hold'em Room Code Multiplayer.
    """

    # Event Message Types
    CREATE_ROOM = "CREATE_ROOM"
    JOIN_ROOM = "JOIN_ROOM"
    ROOM_STATE = "ROOM_STATE"
    START_GAME = "START_GAME"
    GAME_ACTION = "GAME_ACTION"
    STATE_SYNC = "STATE_SYNC"
    CHAT_MESSAGE = "CHAT_MESSAGE"
    ERROR = "ERROR"

    @staticmethod
    def encode(msg_type: str, data: dict = None) -> bytes:
        packet = {
            "type": msg_type,
            "data": data or {}
        }
        raw = json.dumps(packet).encode("utf-8")
        # 4-byte big-endian length prefix for safe streaming
        length_prefix = len(raw).to_bytes(4, byteorder="big")
        return length_prefix + raw

    MAX_PACKET_SIZE = 65536  # 64 KB safety limit for network packets

    @staticmethod
    def decode_stream(stream_buffer: bytearray):
        """
        Extract complete JSON packets from streaming bytearray buffer with size validation.
        """
        packets = []
        while len(stream_buffer) >= 4:
            length = int.from_bytes(stream_buffer[:4], byteorder="big")
            
            # Guard against invalid or oversized packets
            if length > NetworkProtocol.MAX_PACKET_SIZE:
                stream_buffer.clear()
                break
                
            if len(stream_buffer) < 4 + length:
                break
            raw_packet = stream_buffer[4:4 + length]
            del stream_buffer[:4 + length]
            try:
                packet = json.loads(raw_packet.decode("utf-8"))
                if isinstance(packet, dict) and "type" in packet:
                    packets.append(packet)
            except Exception:
                pass
        return packets
