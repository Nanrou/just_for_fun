import unittest
from board import Board1024


class Board1024TestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board1024()

    def test_handle_single_row(self):
        row = [2, '', '', 2]
        self.assertEqual(self.board.handle_single_row(row), [4, '', '', ''])
        row = [2, 2, 4, 4]
        self.assertEqual(self.board.handle_single_row(row), [4, 8, '', ''])
        row = [2, 2, '', '']
        self.assertEqual(self.board.handle_single_row(row), [4, '', '', ''])
        row = [2, 4, 2, 4]
        self.assertEqual(self.board.handle_single_row(row), [2, 4, 2, 4])
        row = ['', '', 2, 2]
        self.assertEqual(self.board.handle_single_row(row), [4, '', '', ''])
        row = [2, 2, '', 4]
        self.assertEqual(self.board.handle_single_row(row), [4, 4, '', ''])
        row = ['', 2, '', 4]
        self.assertEqual(self.board.handle_single_row(row), [2, 4, '', ''])


if __name__ == '__main__':
    unittest.main()
