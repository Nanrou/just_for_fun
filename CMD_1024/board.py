from itertools import chain
from random import randint


def create_board(piece_list):  # 根据传入的参数生成棋盘
    _board = ''
    for _ in range(4):
        _board += '-' * 21 + '\n'
        _board += ('|' + '{:^4}') * 4 + '|' + '\n'
    _board += '-' * 21 + '\n'
    return _board.format(*map(str, piece_list))
    
    
def product_2_or_4():  # 随机返回4或2,33%生成4,66%生成2
    if randint(0, 2) > 1:
        return 4
    else:
        return 2   
    
def product_random_piect(piece_list):  # 在空的地方填数字
    if '' not in piece_list:
        raise GameOverException
    _empty_list = []
    for i, k in enumerate(piece_list):
        if not k:
            _empty_list.append(i)
    _position = _empty_list[randint(0, len(_empty_list))]
    piece_list[_position] = product_2_or_4()
    return piece_list
    
    
def init_list():  # 初始化所有棋子
    init_list = []    
    for _ in range(16):  # TODO 只用一个list去表示
        init_list.append('')
    for _ in range(3):
        init_list = product_random_piect(init_list)  
    return init_list
    
def row_move(piece_list, direction='left'):
    # TODO
    
if __name__ == '__main__':
    nn = init_list()
    print(create_board(nn))
    print(create_board(row_move(nn)))