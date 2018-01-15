import unittest
from unittest import TestCase

from calc_alpha import Interpreter


class TestPascalInterpreter(TestCase):

    def test_plus_sub(self):
        _text = '5+13  -2'
        _interpreter = Interpreter(_text)
        self.assertEqual(_interpreter.expr(), eval(_text))

    def test_mul_div(self):
        _text = '6*13  /2'
        _interpreter = Interpreter(_text)
        self.assertEqual(_interpreter.expr(), eval(_text))

    def test_term(self):
        _text = '2+23  *3'
        _interpreter = Interpreter(_text)
        self.assertEqual(_interpreter.expr(), eval(_text))

    def test_complex_term(self):
        _text = '42/2+2  *3-21'
        _interpreter = Interpreter(_text)
        self.assertEqual(_interpreter.expr(), eval(_text))

    def test_parent(self):
        _text = '4/(2+2 )  *(3 -2)'
        _interpreter = Interpreter(_text)
        self.assertEqual(_interpreter.expr(), eval(_text))


if __name__ == '__main__':
    unittest.main()
