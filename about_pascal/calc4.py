# Token types

"""
获取内容，分词，语法分析，生成部件，组合

独立出一个移动指针向前的方法
过滤空格的方法

先分析语义，通过这一步去生成token
然后在主要控制流，看token是否可以进行操作
最后得到一个不可分解的因子就行了

"""

INTEGER, EOF = 'INTEGER', 'EOF'
PLUS, SUB, MUL, DIV = 'PLUS', 'SUB', 'MUL', 'DIV'
OP = [PLUS, SUB, MUL, DIV]


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return 'Token({_type}, {_value})'.format(_type=self.type, _value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._current_char = self._text[self._pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):  # 最底层的前进动作
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

    def get_next_token(self):  # 通过比较字符串拿到类型
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


class Interpreter:
    def __init__(self, lexer):
        self._lexer = lexer
        self._current_token = self._lexer.get_next_token()

    def error(self):
        raise Exception('Error parsing input')

    def eat(self, token_type):  # 确认类型，并且将移动当前指针，拿到下一个token
        assert hasattr(self._current_token, 'type')
        if self._current_token.type == token_type:
            self._current_token = self._lexer.get_next_token()
        else:
            self.error()

    def factor(self):  # 进行计算，得到数字
        _token = self._current_token
        self.eat(INTEGER)
        return _token.value

    def expr(self):  # 这是主要控制流
        _final_res = self.factor()
        while self._current_token.type in OP:  # 当遇到操作符就意味着后面还有数字
            _op = self._current_token
            if _op.type == PLUS:
                self.eat(PLUS)
                _final_res += self.factor()
            elif _op.type == SUB:
                self.eat(SUB)
                _final_res -= self.factor()
            elif _op.type == MUL:
                self.eat(MUL)
                _final_res *= self.factor()
            else:
                self.eat(DIV)
                _final_res /= self.factor()

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
            lexer = Lexer(text)
            interpreter = Interpreter(lexer)
            result = interpreter.expr()
            print(result)
    except KeyboardInterrupt:
        print('\nbye~')


if __name__ == '__main__':
    main()
