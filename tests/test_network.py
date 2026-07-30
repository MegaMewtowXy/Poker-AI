import time
import unittest
from network.protocol import NetworkProtocol
from network.server import RoomServer
from network.client import NetworkClient

class TestNetworkMultiplayer(unittest.TestCase):

    def setUp(self):
        self.server = RoomServer(host="127.0.0.1", port=9998)
        self.server.start()
        time.sleep(0.1)

    def tearDown(self):
        self.server.stop()

    def test_ip_room_code_encoding(self):
        code = RoomServer.ip_to_room_code("192.168.1.15")
        self.assertEqual(code, "PKR-C0A8010F")
        decoded_ip = RoomServer.room_code_to_ip(code)
        self.assertEqual(decoded_ip, "192.168.1.15")

    def test_create_and_join_room(self):
        client1 = NetworkClient()
        self.assertTrue(client1.connect("127.0.0.1", 9998))
        client1.send(NetworkProtocol.CREATE_ROOM, {"host_name": "HostPlayer", "starting_chips": 1000})
        
        time.sleep(0.2)
        events1 = client1.poll_events()
        self.assertTrue(len(events1) > 0)
        room_state = events1[0]["data"]
        room_code = room_state["room_code"]
        self.assertTrue(room_code.startswith("PKR-"))

        # Client 2 joins using room_code
        client2 = NetworkClient()
        self.assertTrue(client2.connect("127.0.0.1", 9998))
        client2.send(NetworkProtocol.JOIN_ROOM, {"room_code": room_code, "player_name": "FriendPlayer"})

        time.sleep(0.2)
        events2 = client2.poll_events()
        self.assertTrue(len(events2) > 0)
        joined_state = events2[0]["data"]
        self.assertIn("FriendPlayer", joined_state["players"])

        client1.disconnect()
        client2.disconnect()

if __name__ == "__main__":
    unittest.main()
