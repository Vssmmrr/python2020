import unittest
from game import DraughtsField
from player import AIPlayer
import time


class Test(unittest.TestCase):
    def test_simple_situation(self):
        field = DraughtsField()
        field.place_draught(0, 0, True)
        field.place_draught(1, 1, False)
        field.place_draught(3, 3, False)
        player = AIPlayer(field, True, AIPlayer.EASY)
        while field.is_order_white:
            player.obtain_events([])
        self.assertTrue(field.game_over())

    def test_more_difficult_situation(self):
        field = DraughtsField()
        field.place_draught(0, 0, True)
        field.place_draught(1, 1, False)
        field.place_draught(3, 3, False)
        field.place_draught(3, 1, False)
        player = AIPlayer(field, True, AIPlayer.EASY)
        while field.is_order_white:
            player.obtain_events([])
        self.assertFalse(field.game_over())
        self.assertEqual(field.num_black_draughts, 1)

    def test_bot_vs_bot(self):
        field = DraughtsField()
        field.place_default()
        players = list()
        players.append(AIPlayer(field, True, AIPlayer.MEDIUM))
        players.append(AIPlayer(field, False, AIPlayer.EASY))

        while not field.game_over():
            for player in players:
                t = time.perf_counter()
                player.obtain_events([])
                self.assertLessEqual(time.perf_counter() - t, 1)
                if field.game_over():
                    break


if __name__ == '__main__':
    unittest.main()
