"""
获取内容，分词，语法分析，生成部件，组合

独立出一个移动指针向前的方法
过滤空格的方法

先分析语义，通过这一步去生成token
然后在主要控制流，看token是否可以进行操作
最后得到一个不可分解的因子就行了

利用term这个方法加了一层，原本expr的作用就是去处理当前与下一个的关系，现在加了
一层term，就类似递归，term也会去处理下一个与再下一个的关系，也通过while的条件
约束来实现了类似优先级的效果

这里解耦解得非常漂亮

Lexer --(Token)--> Parser --(AST)--> Interpreter
通过Lexer生成token，然后通过parser将token作为一个个结点，构成树，最后解析器通过
遍历树来得到结果

"""
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


class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


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
        if _token.type == INTEGER:
            self.eat(INTEGER)
            return Num(_token)
        elif _token.type == LPARENT:
            self.eat(LPARENT)
            _node = self.expr()  # 递归调用
            self.eat(RPARENT)
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
        while self._current_token.type in (PLUS, SUB):
            _op = self._current_token
            if _op.value == '+':
                self.eat(PLUS)
            elif _op.value == '-':
                self.eat(SUB)

            _node = self.construct_node(left=_node, op=_op, right=self.term())
        return _node

    def parse(self):
        return self.expr()


class NodeVisitor:
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit(self, node):  # 类似适配器，根据不同的method_name去选择不同的方法
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self._parser = parser

    def visit_BinOp(self, node):  # 定义了具体的操作方法
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == SUB:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self._parser.parse()  # 拿到的是树的根结点
        return self.visit(tree)


class RPNTranslator(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree

    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        return '{left} {right} {op}'.format(
            left=left_val, right=right_val, op=node.op.value
        )

    def visit_Num(self, node):
        return node.value

    def translate(self):
        return self.visit(self.tree)


class LISPTranslator(RPNTranslator):
    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        return '{op} {left} {right}'.format(
            left=left_val, right=right_val, op=node.op.value
        )


def main():
    try:
        while True:
            try:
                text = input('spi> ')
            except EOFError:
                break
            if not text:
                continue
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
    except KeyboardInterrupt:
        print('\nbye~')


if __name__ == '__main__':
    main()
