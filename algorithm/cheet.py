from queue import LifoQueue
from copy import deepcopy
import time


def block(matrix, pos):
    i, j = pos
    matrix[pos[0]][pos[1]] = 1

    for col in range(len(matrix)):  # 横向封锁
        if col == j:
            continue
        matrix[i][col] = 2
        if 0 <= i+(col-j) < len(matrix):  # 右斜线
            matrix[i+(col-j)][col] = 2

    for row in range(len(matrix)):  # 纵向封锁
        if row == i:
            continue
        matrix[row][j] = 2   
        if 0 <= j-(row-i) < len(matrix):  # 左斜线
            matrix[row][j-(row-i)] = 2


def queen(n=8):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    stack = LifoQueue()
    time = 0
    for i in range(n):
        stack.put((deepcopy(matrix), (0, i)))  # 一定要用深拷贝来存储这个矩阵
        while not stack.empty():  # 利用栈来回溯
            _matrix, pos = stack.get()
            block(_matrix, pos)

            if pos[0] + 1 == len(_matrix) and 1 in _matrix[-1]:
                # print('*'*10)
                # print('success')
                # for line in _matrix:
                #     print(line)
                # print('*'*10)
                time += 1
            for _row, line in enumerate(_matrix[pos[0]+1:], start=pos[0]+1):
                if 0 in line:
                    for _col, ele in enumerate(line):
                        if ele == 0:
                            stack.put((deepcopy(_matrix), (_row, _col)))
                    break
                else:
                    # print('fail in:', pos)
                    break
    print('success {} times'.format(time))


def queen_one(n, cur=0):
    """
    基于深度优先搜索。
    一维数组中的元素n[i]代表的是第i行，第A[i]列。
    
    外层的循环是为了循环完该行的所有位置。
    内层的循环则是比较该行，与之前行的关系。
    
    理解好其核心是，一旦内层的判断通过，就会以此为起点，向下一行出发。（就是深度优先）
    结束的条件是到达最后一行，因为是先判断再到达，所以一旦到达，就说明最后一行是满足要求的。
    
    最后的输出就是满足条件的，八皇后的位置。
    """

    if cur == len(n):
        print(n)
    else:  
        for col in range(len(n)):
            n[cur] = col  # 表示把第cur行的皇后放在col列上
            for r in range(cur):  
                if n[r] == col \
                        or r-n[r] == cur-n[cur] \
                        or r+n[r] == cur+n[cur]:  # 判断是否跟前面的皇后冲突
                    break  
            else:
                queen_one(n, cur+1)


"""
举一反三：对于这种在可以利用二维数组来存储，但每行只用了一个位置的关系，都可以用一位数组来代替，来达到空间复杂度上的优化。
我最开始的做法是自己建立了一个栈来储存信息，而后面这个做法则是利用了程序的运行栈来保存信息。
前者并不是递归，后者是递归。
递归就是利用程序的运行栈的。

"""


def knight_travel(n=5, start=(2, 2)):
    assert int(n) > 4
    dirs = [(-1, -2), (1, -2), (-2, -1), (2, -1), (-2, 1), (2, 1), (-1, 2), (1, 2)]

    def mark(maze, pos):  # 标记该位
        maze[pos[0]][pos[1]] = 1

    def possible(maze, pos):  # 判断合法性
        if -1 < pos[0] < n and -1 < pos[1] < n and maze[pos[0]][pos[1]] == 0:
            return True
        return False

    def done(maze):  # 判断是否已结束
        return all(all(_i == 1 for _i in row) for row in maze)

    _maze = [[0 for _ in range(n)] for _ in range(n)]
    stack = LifoQueue()
    mark(_maze, start)
    stack.put((deepcopy(_maze), start, 0))
    while not stack.empty():
        _maze, _pos, nxt = stack.get()
        for i in range(nxt, len(dirs)):
            nextp = (_pos[0] + dirs[i][0], _pos[1] + dirs[i][1])
            if done(_maze):
                print(stack.queue)  # 栈中存储的就是答案，之前的做法应该没错，只是要太长时间了，这个运行了70000+次
                print('done')
                return
            if possible(_maze, nextp):
                stack.put((deepcopy(_maze), _pos, i + 1))
                mark(_maze, nextp)
                stack.put((deepcopy(_maze), nextp, 0))
                break
    else:
        print(_maze)
        print('false')


if __name__ == '__main__':
    # matrix = [[0 for _ in range(4)] for _ in range(4)]
    # for line in block(matrix, (0, 0)):
    #    print(line)
    # queen_one([None]*8)
    # queen()
    knight_travel(5)
