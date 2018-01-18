(INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN,
 BEGIN, END, SEMI, DOT, EOF) = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'ID', 'ASSIGN',
    'BEGIN', 'END', 'SEMI', 'DOT', 'EOF'
)


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
}


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

    def peek(self):  # 看再下一个位置而不移动指针
        _peek_pos = self._pos + 1
        if _peek_pos > len(self._text) - 1:
            return None
        else:
            return self._text[_peek_pos]

    def skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self.advance()

    def multi_number(self):
        _number = ''
        while self._current_char is not None and self._current_char.isdigit():
            _number += self._current_char
            self.advance()
        return int(_number)

    def _id(self, underscore=False):
        _identifier = '' if not underscore else '_'
        while self._current_char is not None and self._current_char.isalnum():
            _identifier += self._current_char
            self.advance()
        # 因为pascal是大小写不敏感的，所以要转换一下
        _token = RESERVED_KEYWORDS.get(_identifier.upper(), Token(ID, _identifier.upper()))
        print(_token)
        return _token

    def get_next_token(self):
        while self._current_char is not None:

            if self._current_char.isspace():
                self.skip_whitespace()
                continue

            if self._current_char == '_' and self.peek().isalpha():
                self.advance()
                return self._id(True)

            if self._current_char.isalpha():
                return self._id()

            if self._current_char.isdigit():
                return Token(INTEGER, self.multi_number())

            if self._current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self._current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self._current_char == '+':
                self.advance()  # 注意这里是要移动指针的
                return Token(PLUS, '+')

            if self._current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self._current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self._current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self._current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self._current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self._current_char == '.':
                self.advance()
                return Token(DOT, '.')

            self.error()

        return Token(EOF, None)


class AST:
    pass


class UnaryOp(AST):  # 一元操作符，作用是让数字为正或负
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser:
    def __init__(self, lexer):
        self._lexer = lexer
        self._current_token = self._lexer.get_next_token()

    def error(self):
        raise Exception('interpreter error')

    def eat(self, token_type):  # 处理完当前token，向下走
        if self._current_token.type == token_type:
            self._current_token = self._lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        _token = self._current_token

        if _token.type == PLUS:
            self.eat(PLUS)
            _node = UnaryOp(_token, self.factor())
            return _node
        elif _token.type == MINUS:
            self.eat(MINUS)
            _node = UnaryOp(_token, self.factor())
            return _node

        if _token.type == INTEGER:
            self.eat(INTEGER)
            return Num(_token)
        elif _token.type == LPAREN:
            self.eat(LPAREN)
            _node = self.expr()  # 递归调用
            self.eat(RPAREN)
            return _node

        _node = self.variable()
        return _node

    @staticmethod
    def construct_node(left, op, right):
        return BinOp(left=left, op=op, right=right)

    def term(self):
        _node = self.factor()
        while self._current_token.type in (MUL, DIV):
            _op = self._current_token
            if _op.value == '*':
                self.eat(MUL)
            elif _op.value == '/':
                self.eat(DIV)

            _node = self.construct_node(left=_node, op=_op, right=self.factor())  # 主要是通过这步生成子树，然后递归结合起来生成语法树
        return _node

    def expr(self):
        _node = self.term()
        while self._current_token.type in (PLUS, MINUS):
            _op = self._current_token
            if _op.value == '+':
                self.eat(PLUS)
            elif _op.value == '-':
                self.eat(MINUS)

            _node = self.construct_node(left=_node, op=_op, right=self.term())
        return _node

    def parse(self):
        _node = self.program()
        if self._current_token.type != EOF:
            self.error()
        return _node

    @staticmethod
    def empty():
        return NoOp()

    def variable(self):
        _node = Var(self._current_token)
        self.eat(ID)
        return _node

    def assignment_statement(self):
        _left = self.variable()
        _token = self._current_token
        self.eat(ASSIGN)
        _right = self.expr()
        _node = Assign(_left, _token, _right)
        return _node

    def statement(self):
        if self._current_token.type == BEGIN:
            _node = self.compound_statement()
        elif self._current_token.type == ID:
            _node = self.assignment_statement()
        else:
            _node = self.empty()

        return _node

    def statement_list(self):
        _node = self.statement()
        _res = [_node]

        while self._current_token.type == SEMI:  # 最后一句是可以不用分号的
            self.eat(SEMI)
            _res.append(self.statement())

        if self._current_token == ID:
            self.error()

        return _res

    def compound_statement(self):
        self.eat(BEGIN)
        _nodes = self.statement_list()
        self.eat(END)

        _root = Compound()
        for _node in _nodes:
            _root.children.append(_node)

        return _root

    def program(self):
        _node = self.compound_statement()
        self.eat(DOT)
        return _node


class NodeVisitor:
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit(self, node):  # 类似适配器，根据不同的method_name去选择不同的方法
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self._parser = parser

    def visit_BinOp(self, node):  # 定义了具体的操作方法
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)  # 单纯地取相反数而已

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self._parser.parse()  # 拿到的是树的根结点
        if tree is None:
            return ''
        return self.visit(tree)


if __name__ == '__main__':
    tt = '''\
BEGIN
    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number / 4;
        c := a - - b
    END;
    x := 11;
END.
'''
    tt2 = """\
BEGIN

    BEGIN
        number := 2;
        a := NumBer;
        B := 10 * a + 10 * NUMBER / 4;
        _c := a - - b
    end;

    x := 11;
END.
"""

    lexer = Lexer(tt2)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)
