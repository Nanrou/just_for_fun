"""
命令行版的打砖块
其实就是通过刷新来输出达到动画效果。
"""

import os
import sys
from random import sample
import time
from itertools import chain, product
from msvcrt import getwch, kbhit
import threading

MAX_LENGTH = 78
MAX_HEIGHT = 25


class GameOverException(Exception):
    def __init__(self, value):
        self.value = value


class Ball:
    def __init__(self, move_range_length, move_range_height):
        self.x = 37
        self.y = 22
        self.is_active = False
        self.width = 1
        self.symbol = '@'
        self.speedX = 1
        self.speedY = 1

        self.move_range_length, self.move_range_height = move_range_length, move_range_height

    def fire(self):
        """激活后才开始运动"""
        self.is_active = True

    def move(self):
        """到达边界就自动反向"""
        if self.x == 0 or self.x == self.move_range_length - 1:
            self.speedX *= -1
        if self.y == 0 or self.y == self.move_range_height - 1:
            self.speedY *= -1
            
        self.x += self.speedX
        self.y += self.speedY


class Block:
    def __init__(self, global_length):
        self.x = 35
        self.y = 23
        self.width = 7
        self.symbol = '='
        self.speed = 2

        self.global_length = global_length

    def move(self, direction='left'):
        """滑板的移动方法"""
        if direction == 'left':
            if self.x - self.speed > 0:
                self.x -= self.speed
            else:
                self.x = 0
        if direction == 'right':
            if self.x + self.width + self.speed < self.global_length:
                self.x += self.speed
            else:
                self.x = self.global_length - self.width - 1
                
    def collide(self, ball):
        """与球碰撞的判断"""
        if self.x <= ball.x <= self.x + self.width and self.y - 1 == ball.y:
            ball.speedY *= -1


class Brick:
    def __init__(self, x, y, width=5):
        self.x = x
        self.y = y
        self.width = width
        self.symbol = '#'

        self.is_alive = True

    def collide(self, ball):
        """砖块与球的碰撞判断"""
        if self.y == ball.y and self.x <= ball.x <= self.x + self.width:
            ball.speedY *= -1
            self.is_alive = False

    @classmethod
    def product_brick(cls, range_length, range_height, width=5, num=5):
        """生成随机砖块的类方法"""
        # 将目标区域分成若干块，然后随机选择块来放砖块
        coord_list = sample(list(product(range(0, range_length-width, width), range(range_height))), num)
        brick_list = []
        for coord in coord_list:
            brick_list.append(Brick(*coord))
        return brick_list


class Main:
    def __init__(self):
        self.length = MAX_LENGTH
        self.height = MAX_HEIGHT

        self.ball = Ball(self.length, self.height)
        self.block = Block(self.length)
        self.bricks = Brick.product_brick(self.length, 5)

        self.write, self.flush = sys.stdout.write, sys.stdout.flush

    def pro_init_list(self):
        """初始化数据列表，数据列表是一个二维列表，以此来代替xy坐标"""
        _data_list = []
        for _ in range(self.height):
            _tmp = []
            for _ in range(self.length):
                _tmp.append(' ')
            _data_list.append(_tmp)
        return _data_list

    def update(self):
        """刷新数据列表的数据，其实就是生成一个新的列表，重新赋值"""
        data_list = self.pro_init_list()
        self.update_obj(self.ball, data_list)
        self.update_obj(self.block, data_list)
        self.bricks = [brick for brick in self.bricks if brick.is_alive]  # 去除死掉的砖块
        for brick in self.bricks:
            self.update_obj(brick, data_list)
        return data_list

    @staticmethod
    def update_obj(obj, ele_list):
        """将坐标换成二列列表的序号"""
        for i in range(obj.width):
            try:
                ele_list[obj.y][obj.x+i] = obj.symbol
            except IndexError:
                print(obj, obj.y, obj.x + i)
                raise RuntimeError

    def draw(self, ctn, wrong_txt):
        """将数据列表输出为目标形式"""
        _ss = ''
        _ss += '-' * int(self.length + 2) + '\n'
        for _ in range(self.height):
            _ss += '|' + '{}' * int(self.length) + '|' + '\n'
        _ss += '-' * int(self.length + 2) + '\n'
        os.system('cls')
        self.write(_ss.format(*chain.from_iterable(ctn)) + '\nball.x={}, ball.y={}\nblock.x={}, block.y={}\n'.format(
            self.ball.x, self.ball.y, self.block.x, self.block.y
        ) + wrong_txt)
        self.flush()

    def run(self):
        """主循环，监听键盘事件，持续刷新"""
        opt_dict = {'a': 'left', 'd': 'right'}
        while True:
            time.sleep(1/30)  # 帧数

            wrong_txt = ''
            if kbhit():  # 监听键盘
                g = getwch()
                if g == 'e':
                    break
                elif g == 'f':  # 激活球的运动状态
                    self.ball.fire()
                elif g in 'ad':  # 移动滑板
                    self.block.move(opt_dict[g])
                else:
                    wrong_txt = 'please input right operation!'

            if self.ball.is_active:  # 判断球是否是运动状态
                self.block.collide(self.ball)  # 判断滑板与球是否碰撞
                if self.bricks:  # 判断是否还有活着的砖块
                    for brick in self.bricks:
                        brick.collide(self.ball)  # 判断砖块与球是否碰撞
                else:  # 没有活的砖块，游戏就胜利了
                    raise GameOverException('Winner Winner, Chicken Dinner!')
                self.ball.move()  # 球运动
                if self.ball.y > self.block.y:  # 球掉到滑板以下就结束了
                    raise GameOverException('GG,WP')
            else:
                self.ball.x = self.block.x + 3  # 非运动状态的时候，球应该一直在滑板上

            self.draw(self.update(), wrong_txt)  # 刷新

    def run_thread(self):
        self.signal = False  # 用这个属性作为信号量，来进行线程间通信
        run_event = threading.Thread(target=self.thread_event_loop)
        run_event.start()  # 开始刷新的主循环
        self.listen_kb()  # 监听键盘
        run_event.join()

    def listen_kb(self):
        opt_dict = {'a': 'left', 'd': 'right'}
        while 1:
            g = getwch()
            if g == 'e':
                self.signal = True
                break
            elif g == 'f':  # 激活球的运动状态
                self.ball.fire()
            elif g in 'ad':  # 移动滑板
                self.block.move(opt_dict[g])
            if self.signal:
                break

    def thread_event_loop(self, wrong_txt=''):
        try:
            while True:
                if self.signal:
                    break
                time.sleep(1/30)  # 帧数
                if self.ball.is_active:  # 判断球是否是运动状态
                    self.block.collide(self.ball)  # 判断滑板与球是否碰撞
                    if self.bricks:  # 判断是否还有活着的砖块
                        for brick in self.bricks:
                            brick.collide(self.ball)  # 判断砖块与球是否碰撞
                    else:  # 没有活的砖块，游戏就胜利了
                        raise GameOverException('Winner Winner, Chicken Dinner!')
                    self.ball.move()  # 球运动
                    if self.ball.y > self.block.y:  # 球掉到滑板以下就结束了
                        raise GameOverException('GG,WP')
                else:
                    self.ball.x = self.block.x + 3  # 非运动状态的时候，球应该一直在滑板上

                self.draw(self.update(), wrong_txt)  # 刷新
        except GameOverException as e:
            self.signal = True
            print('\n' + e.value + '\n' + '按任意键退出')


if __name__ == '__main__':
    main = Main()
    # main.run()
    main.run_thread()
