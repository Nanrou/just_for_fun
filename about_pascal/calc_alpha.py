#! /bin/python

INTEGER, EOF = 'integer', 'eof'
PLUS, SUB, MUL, DIV = 'plus', 'sub', 'mul', 'div'
LPARENT, RPARENT = '(', ')'


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type, self.value)

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._current_char = self._text[self._pos]

    def error(self):
        raise Exception('Invalid Input')

    def advance(self):
        self._pos += 1
        if self._pos < len(self._text):
            self._current_char = self._text[self._pos]
        else:
            self._current_char = None

    def skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self.advance()

    def multi_number(self):
        _number = ''
        while self._current_char is not None and self._current_char.isdigit():
            _number += self._current_char
            self.advance()
        return int(_number)

    def get_next_token(self):
        while self._current_char is not None:
            self.skip_whitespace()

            if self._current_char.isdigit():
                return Token(INTEGER, self.multi_number())

            if self._current_char == '+':
                self.advance()  # 注意这里是要移动指针的
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

            if self._current_char == '(':
                self.advance()
                return Token(LPARENT, '(')

            if self._current_char == ')':
                self.advance()
                return Token(RPARENT, ')')

            self.error()

        return Token(EOF, None)


"""
主要逻辑是，局部保存当前值，然后手动取下个值来操作
"""


class Interpreter:
    def __init__(self, text):
        self._lexer = Lexer(text)
        self._current_token = self._lexer.get_next_token()

    def error(self):
        raise Exception('interpreter error')

    def eat(self, token_type):  # 处理完当前token，向下走
        if self._current_token.type == token_type:
            self._current_token = self._lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        if self._current_token.type == INTEGER:
            _value = self._current_token.value
            self.eat(INTEGER)
            return _value
        elif self._current_token.type == LPARENT:
            self.eat(LPARENT)
            _res = self.expr()   # 递归调用
            self.eat(RPARENT)
            return _res

    def term(self):
        _res = self.factor()
        while self._current_token.type in (MUL, DIV):
            _op = self._current_token.value
            if _op == '*':
                self.eat(MUL)
                _res *= self.factor()
            elif _op == '/':
                self.eat(DIV)
                _res /= self.factor()
        return _res

    def expr(self):
        _res = self.term()
        while self._current_token.type in (PLUS, SUB):
            _op = self._current_token.value
            if _op == '+':
                self.eat(PLUS)
                _res += self.term()
            elif _op == '-':
                self.eat(SUB)
                _res -= self.term()
        return _res


if __name__ == '__main__':
    pass
