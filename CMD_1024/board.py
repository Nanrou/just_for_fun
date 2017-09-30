from random import randint
import sys
import os

from get_single_input import getch


class GameOverException(Exception):
    """游戏结束"""
    def __init__(self, value):
        self.value = value


class Board1024:
    def __init__(self):
        self.score = 0
        self.piece_list = self.init_list()
        self.opt_dict = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}
        self.write, self.flush = sys.stdout.write, sys.stdout.flush

    def init_list(self):  # 初始化所有棋子
        _init_list = []
        for _ in range(16):
            _init_list.append('')
        for _ in range(3):
            _init_list = self.product_random_piece(_init_list)
        return _init_list

    @staticmethod
    def product_2_or_4():  # 随机返回4或2,33%生成4,66%生成2
        if randint(0, 2) > 1:
            return 4
        else:
            return 2

    def product_random_piece(self, piece_list=None):  # 在空的地方填数字
        if piece_list is None:
            piece_list = self.piece_list
        _empty_list = []
        for i, k in enumerate(piece_list):
            if not k:
                _empty_list.append(i)
        _position = _empty_list[0 if len(_empty_list) == 1 else randint(0, len(_empty_list) - 1)]
        piece_list[_position] = self.product_2_or_4()
        return piece_list

    def handle_single_row(self, single_list):
        pp = list(single_list)
        llen = len(pp)
        while True:
            if '' not in pp:
                break
            pp.remove('')
        for i in range(len(pp) - 1):
            if pp[i] == pp[i+1]:
                pp[i] *= 2
                self.score += pp[i]
                pp[i+1] = ''
        while True:
            if '' not in pp:
                break
            pp.remove('')
        for _ in range(llen - len(pp)):
            pp.append('')
        return pp

    def operation(self, piece_list=None, opt='left'):
        if piece_list is None:
            piece_list = self.piece_list
        if opt == 'left':
            for i in range(4):
                piece_list[i*4: i*4 + 4] = self.handle_single_row(piece_list[i*4: i*4 + 4])
        elif opt == 'right':
            for i in range(4):
                piece_list[i*4: i*4 + 4] = reversed(self.handle_single_row(reversed(piece_list[i*4: i*4 + 4])))
        elif opt == 'up':
            for i in range(4):
                piece_list[i], piece_list[i + 4], piece_list[i + 8], piece_list[i + 12] = self.handle_single_row(
                    [piece_list[i], piece_list[i + 4], piece_list[i + 8], piece_list[i + 12]]
                )
        elif opt == 'down':
            for i in range(4):
                piece_list[i], piece_list[i + 4], piece_list[i + 8], piece_list[i + 12] = reversed(self.handle_single_row(
                    reversed([piece_list[i], piece_list[i + 4], piece_list[i + 8], piece_list[i + 12]])
                ))
        return piece_list

    def create_board(self, piece_list=None):
        if piece_list is None:
            piece_list = self.piece_list
        _board = ''
        for _ in range(4):
            _board += '-' * 21 + '\n'
            _board += ('|' + '{:^4}') * 4 + '|' + '\n'
        _board += '-' * 21 + '\n'
        return _board.format(*map(str, piece_list))

    def still_alive(self, piece_list=None):
        if piece_list is None:
            piece_list = self.piece_list
        if 1024 in piece_list:
            raise GameOverException('Winner Winner, Chicken Dinner!')
        if '' in piece_list:
            return True
        if [piece_list[1], piece_list[4:7], piece_list[9]].count(piece_list[5]) > 1:
            return True
        if [piece_list[6], piece_list[9:12], piece_list[14]].count(piece_list[10]) > 1:
            return True
        if [piece_list[2:4], piece_list[7]].count(piece_list[4]):
            return True
        if [piece_list[12:14], piece_list[8]].count(piece_list[12]):
            return True
        if [piece_list[0:2], piece_list[4]].count(piece_list[0]):
            return True
        if [piece_list[14:], piece_list[11]].count(piece_list[15]):
            return True
        raise GameOverException('GG, WP')

        # piece_set = set(piece_list)
        # for item in piece_set:
        #     if piece_list.count(item) > 1:

    def draw(self, ctn, wrong_txt=''):
        os.system('cls')
        title_txt = '{:^21}\n'.format('Game of 1024')
        score_txt = 'Score: %d point!\n' % self.score
        help_txt = 'operation: wasd\nexit:e\n'
        ctn = ''.join([title_txt, ctn, score_txt, help_txt, wrong_txt])
        self.write(ctn)
        self.flush()

    def run(self):
        os.system('cls')
        wrong_txt = ''
        while True:
            _board = self.create_board()
            self.draw(_board, wrong_txt)

            try:
                self.still_alive()
            except GameOverException as e:
                self.write(e.value)
                self.flush()
                break

            g = getch()
            wrong_txt = ''
            if g == 'e':
                break
            elif g in 'wasd':
                self.operation(opt=self.opt_dict[g])
                self.product_random_piece()
            else:
                wrong_txt = 'please input right operation!'


if __name__ == '__main__':
    # ll = ([2, '', '', 2], ['', 4, '', 2], ['', '', 2, 2], [2, 2, 4, 4], [2, 2, '', ''], [2, 4, 2, 4], [2, 2, '', 4])
    # for l in ll:
    #     print(l, handle_single_row(l))
    # g = getch()
    # print(g)
    board = Board1024()
    board.run()
