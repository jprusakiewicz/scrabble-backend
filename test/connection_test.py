import json
import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.color import Color


class ConnectionManagerTest(unittest.TestCase):
    def test_single_connection(self):
        # given
        client = TestClient(app)
        test_client_id = 1
        test_room_id = 1
        expected_game_state = False
        expected_game_data = []
        expected_whos_turn = 0
        # when
        with client.websocket_connect(f"/ws/{test_room_id}/{test_client_id}") as websocket:
            data = websocket.receive_json()
        # then
        self.assertEqual(data['is_game_on'], expected_game_state)

    def test_double_connection(self):
        # given
        client = TestClient(app)
        test_client_one_id = 1
        test_client_two_id = 2
        test_room_id = 1
        expected_game_state = False
        expected_whos_turn = [c.value for c in Color]
        # when
        with client.websocket_connect(f"/ws/{test_room_id}/{test_client_one_id}") as websocket:
            _ = websocket.receive_json()

            with client.websocket_connect(f"/ws/{test_room_id}/{test_client_two_id}") as websocket:
                data = websocket.receive_json()
        # then
        self.assertEqual(data['is_game_on'], expected_game_state)
        self.assertIn(data['whos_turn'], expected_whos_turn)
        self.assertNotIsInstance(data['game_data'], str)

    # def test_picking_card(self):
    #     # given
    #     client = TestClient(app)
    #     test_client_one_id = 1
    #     test_client_two_id = 2
    #     test_room_id = 1
    #     expected_game_state = True
    #     expected_game_data = ["U+F0A1"]
    #     expected_whos_turn = "left"
    #     # when
    #     with client.websocket_connect(f"/ws/{test_room_id}/{test_client_one_id}") as websocket1:
    #         _ = websocket1.receive_json()
    #
    #         with client.websocket_connect(f"/ws/{test_room_id}/{test_client_two_id}") as websocket2:
    #             data21 = websocket2.receive_json()
    #             data11 = websocket1.receive_json()
    #
    #             assert data21['whos_turn'] == 'right'
    #             websocket1.send_json({"picked_cards": [data11['game_data']['player_hand'][0]]})
    #             data12 = websocket1.receive_json()
    #             data22 = websocket2.receive_json()
    #
    #     # then
    #     self.assertEqual(data12["game_data"]["pile"][0], data11['game_data']['player_hand'][0])
    #     self.assertEqual(data12['is_game_on'], expected_game_state)
    #     self.assertEqual(data12['whos_turn'], expected_whos_turn)
    #     self.assertEqual(data12['game_data']['player_hand'], data12['game_data']['player_hand'][0:])
    #
    # def test_picking_card_not_in_hand(self):
    #     # given
    #     client = TestClient(app)
    #     test_client_one_id = 1
    #     test_client_two_id = 2
    #     test_room_id = 1
    #     expected_game_state = True
    #     expected_game_data = ["U+F0A1"]
    #     expected_whos_turn = "2"
    #     # when
    #     with client.websocket_connect(f"/ws/{test_room_id}/{test_client_one_id}") as websocket1:
    #         _ = websocket1.receive_json()
    #
    #         with client.websocket_connect(f"/ws/{test_room_id}/{test_client_two_id}") as websocket2:
    #             data21 = websocket2.receive_json()
    #             data12 = websocket1.receive_json()
    #
    #             assert data21['whos_turn'] == '1'
    #             websocket1.send_json({"picked_cards": ["U+F0A1"]})
    #             data12 = websocket1.receive_json()
    #             data22 = websocket2.receive_json()
    #
    #     # then
    #     self.assertEqual(data22["game_data"]["pile"], "U+F0A1")
    #     self.assertEqual(data22['is_game_on'], expected_game_state)
    #     self.assertEqual(data22['whos_turn'], expected_whos_turn)
    #     self.assertEqual(data22['game_data'], expected_game_data)

    def test_sending_turn_by_wrong_player(self):
        ...

    def test_reconnect(self):
        client = TestClient(app)
        test_client_id = 1
        expected_game_state = False
        expected_game_data = ''
        expected_whos_turn = 0
        # when

        with client.websocket_connect(f"/ws/{test_client_id}") as websocket:
            _ = websocket.receive_json()

        with client.websocket_connect(f"/ws/{test_client_id}") as websocket:
            data = websocket.receive_json()
        # then
        self.assertEqual(data['is_game_on'], expected_game_state)
        self.assertEqual(data['whos_turn'], expected_whos_turn)
        self.assertEqual(data['game_data'], expected_game_data)

    def test_double_connection_with_same_id(self):
        # given
        client = TestClient(app)
        test_client_one_id = 1
        test_client_two_id = 1

        # when
        try:
            with client.websocket_connect(f"/ws/{test_client_one_id}") as websocket:
                _ = websocket.receive_json()

                with client.websocket_connect(f"/ws/{test_client_two_id}") as websocket:
                    data = websocket.receive_json()
        except Exception as e:
            exception = e
        # then
        self.assertEqual(exception.__class__.__name__, websockets.WebSocketDisconnect(403).__class__.__name__)

    if __name__ == '__main__':
        unittest.main()
