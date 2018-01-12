# Token types

"""
获取内容，分词，语法分析，生成部件，组合

独立出一个移动指针向前的方法
过滤空格的方法

"""

INTEGER, EOF = 'INTEGER', 'EOF'
OP = ['PLUS', 'SUB']
PLUS, SUB, MUL, DIV = 'PLUS', 'SUB', 'MUL', 'DIV'


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return 'Token({_type}, {_value})'.format(_type=self.type, _value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Interpreter:
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._current_token = None
        self._current_char = self._text[self._pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self._pos += 1
        if self._pos > len(self._text) - 1:
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self.advance()

    def integer(self):
        _res = ''
        while self._current_char is not None and self._current_char.isdigit():
            _res += self._current_char
            self.advance()
        return int(_res)

    def get_next_token(self):
        while self._current_char is not None:
            if self._current_char.isspace():
                self.skip_whitespace()
                continue

            if self._current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self._current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self._current_char == '-':
                self.advance()
                return Token(SUB, '-')

            if self._current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self._current_char == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        assert hasattr(self._current_token, 'type')
        if self._current_token.type == token_type:
            self._current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):  # 这是主要控制流
        _final_res = None
        while self._pos < len(self._text):

            if _final_res is None:
                _left = self._current_token = self.get_next_token()
                self.eat(INTEGER)
            else:
                _left = Token(INTEGER, _final_res)

            _op = self._current_token
            if _op.type == PLUS:
                self.eat(PLUS)
            elif _op.type == SUB:
                self.eat(SUB)
            elif _op.type == MUL:
                self.eat(MUL)
            else:
                self.eat(DIV)

            _right = self._current_token
            self.eat(INTEGER)

            if _op.type == PLUS:
                _final_res = _left.value + _right.value
            elif _op.type == SUB:
                _final_res = _left.value - _right.value
            elif _op.type == MUL:
                _final_res = _left.value * _right.value
            else:
                _final_res = _left.value / _right.value

        return _final_res


def main():
    try:
        while True:
            try:
                text = input('calc> ')
            except EOFError:
                break
            if not text:
                continue
            interpreter = Interpreter(text)
            result = interpreter.expr()
            print(result)
    except KeyboardInterrupt:
        print('\nbye~')


if __name__ == '__main__':
    main()
