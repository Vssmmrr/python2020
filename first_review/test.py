import unittest
from game import DraughtsField
from player import AIPlayer
import time


class Test(unittest.TestCase):
    def test_simple_situation(self):
        field = DraughtsField()
        field.place_draught(0, 0, field.WHITE)
        field.place_draught(1, 1, field.BLACK)
        field.place_draught(3, 3, field.BLACK)
        player = AIPlayer(field, field.WHITE, AIPlayer.EASY)
        while field.order == field.WHITE:
            player.obtain_events([])
        self.assertTrue(field.game_over())

    def test_more_difficult_situation(self):
        field = DraughtsField()
        field.place_draught(0, 0, field.WHITE)
        field.place_draught(1, 1, field.BLACK)
        field.place_draught(3, 3, field.BLACK)
        field.place_draught(3, 1, field.BLACK)
        player = AIPlayer(field, field.WHITE, AIPlayer.EASY)
        while field.order == field.WHITE:
            player.obtain_events([])
        self.assertFalse(field.game_over())
        self.assertEqual(field.num_black_draughts, 1)

    def test_bot_vs_bot(self):
        field = DraughtsField()
        field.place_default()
        players = list()
        players.append(AIPlayer(field, field.WHITE, AIPlayer.MEDIUM))
        players.append(AIPlayer(field, field.BLACK, AIPlayer.EASY))

        while not field.game_over():
            for player in players:
                t = time.perf_counter()
                player.obtain_events([])
                self.assertLessEqual(time.perf_counter() - t, 1)
                if field.game_over():
                    break


if __name__ == '__main__':
    unittest.main()
