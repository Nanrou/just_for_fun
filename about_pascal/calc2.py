# Token types

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

    def term(self):
        _token = self._current_token
        self.eat(INTEGER)
        return _token.value

    def expr(self):
        self._current_token = self.get_next_token()
        _final_res = self.term()
        while self._current_token.type in OP:
            _op = self._current_token
            if _op.type == PLUS:
                self.eat(PLUS)
                _final_res += self.term()
            elif _op.type == SUB:
                self.eat(SUB)
                _final_res -= self.term()
            elif _op.type == MUL:
                self.eat(MUL)
                _final_res *= self.term()
            else:
                self.eat(DIV)
                _final_res //= self.term()

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
