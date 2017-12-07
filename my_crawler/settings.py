import os
import logging
from logging import Logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MyLogger(Logger):
    def __init__(self, name='logger'):
        super(MyLogger, self).__init__(name)
        self.setLevel = logging.DEBUG

        self.ch = logging.StreamHandler()
        self.datefmt = '%Y-%m-%d %H:%M:%S'
        self.formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s', self.datefmt)
        self.ch.setFormatter(self.formatter)
        self.addHandler(self.ch)

        self.fh = logging.FileHandler(os.path.join(BASE_DIR, 'warning.log'), encoding='utf-8')
        self.fh.setLevel(logging.WARNING)
        self.fh.setFormatter(self.formatter)
        self.addHandler(self.fh)
