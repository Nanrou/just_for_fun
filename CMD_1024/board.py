from random import randint
import sys
import os

from get_single_input import getch


class GameOverException(Exception):
    """游戏结束"""


def create_board(piece_list):  # 根据传入的参数生成棋盘
    _board = ''
    for _ in range(4):
        _board += '-' * 21 + '\n'
        _board += ('|' + '{:^4}') * 4 + '|' + '\n'
    _board += '-' * 21 + '\n'
    return _board.format(*map(str, piece_list))


def still_alive(piece_list):
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
    return False

    # piece_set = set(piece_list)
    # for item in piece_set:
    #     if piece_list.count(item) > 1:


def product_2_or_4():  # 随机返回4或2,33%生成4,66%生成2
    if randint(0, 2) > 1:
        return 4
    else:
        return 2   


def product_random_piece(piece_list):  # 在空的地方填数字
    _empty_list = []
    for i, k in enumerate(piece_list):
        if not k:
            _empty_list.append(i)
    _position = _empty_list[randint(0, len(_empty_list) - 1)]
    piece_list[_position] = product_2_or_4()
    return piece_list
    
    
def init_list():  # 初始化所有棋子
    _init_list = []
    for _ in range(16):
        _init_list.append('')
    for _ in range(3):
        _init_list = product_random_piece(_init_list)
    return _init_list


def handle_single_row(single_list):
    pp = list(single_list)
    llen = len(pp)
    while True:
        if '' not in pp:
            break
        pp.remove('')
    for i in range(len(pp) - 1):
        if pp[i] == pp[i+1]:
            pp[i] *= 2
            pp[i+1] = ''
    while True:
        if '' not in pp:
            break
        pp.remove('')
    for _ in range(llen - len(pp)):
        pp.append('')
    return pp


def operation(piece_list, opt='left'):
    if opt == 'left':
        for i in range(4):
            piece_list[i*4: i*4 + 4] = handle_single_row(piece_list[i*4: i*4 + 4])
    elif opt == 'right':
        for i in range(4):
            piece_list[i*4: i*4 + 4] = reversed(handle_single_row(reversed(piece_list[i*4: i*4 + 4])))
    elif opt == 'up':
        for i in range(4):
            piece_list[i], piece_list[i + 4], piece_list[i + 8], piece_list[i + 12] = handle_single_row(
                [piece_list[i], piece_list[i + 4], piece_list[i + 8], piece_list[i + 12]]
            )
    elif opt == 'down':
        for i in range(4):
            piece_list[i], piece_list[i + 4], piece_list[i + 8], piece_list[i + 12] = reversed(handle_single_row(
                reversed([piece_list[i], piece_list[i + 4], piece_list[i + 8], piece_list[i + 12]])
            ))
    return piece_list


opt_dict = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}


def main():
    write, flush = sys.stdout.write, sys.stdout.flush
    piece_list = init_list()
    os.system('cls')
    while True:
        board = create_board(piece_list)
        write(board)
        flush()

        if not still_alive(piece_list):
            raise GameOverException

        g = getch()

        if g == 'e':
            break
        if g in 'wasd':
            piece_list = product_random_piece(operation(piece_list, opt_dict[g]))
        os.system('cls')


if __name__ == '__main__':
    # nn = init_list()
    # print(create_board(nn))
    # print(create_board(operation(nn, opt='down')))
    # ll = ([2, '', '', 2], ['', 4, '', 2], ['', '', 2, 2], [2, 2, 4, 4], [2, 2, '', ''], [2, 4, 2, 4], [2, 2, '', 4])
    # for l in ll:
    #     print(l, handle_single_row(l))
    main()
    # g = getch()
    # print(g)
