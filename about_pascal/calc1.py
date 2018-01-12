# Token types

INTEGER, EOF = 'INTEGER', 'EOF'
OP = ['PLUS', 'SUB']
PLUS, SUB = 'PLUS', 'SUB'


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

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        _text = self._text
        if self._pos > len(_text) - 1:
            return Token(EOF, None)

        _current_char = _text[self._pos]
        try:
            while True:
                if _current_char.isspace():  # 无视空格
                    self._pos += 1
                    _current_char = _text[self._pos]
                else:
                    break
        except IndexError:
            return Token(EOF, None)

        if _current_char.isdigit():
            _tmp = _current_char
            try:
                while True:
                    if _text[self._pos + 1].isdigit():  # 取非个位数
                        self._pos += 1
                        _tmp += _text[self._pos]
                    else:
                        break
            except IndexError:
                pass
            _token = Token(INTEGER, int(_tmp))
            self._pos += 1
            return _token

        if _current_char == '+':
            _token = Token(PLUS, _current_char)
            self._pos += 1
            return _token

        if _current_char == '-':
            _token = Token(SUB, _current_char)
            self._pos += 1
            return _token

        self.error()

    def eat(self, token_type):
        assert hasattr(self._current_token, 'type')
        if self._current_token.type == token_type or self._current_token.type in OP:
            self._current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self._current_token = self.get_next_token()

        _left = self._current_token
        self.eat(INTEGER)

        _op = self._current_token
        self.eat(OP)

        _right = self._current_token
        self.eat(INTEGER)
        if _op.value == '+':
            return _left.value + _right.value
        else:
            return _left.value - _right.value


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
