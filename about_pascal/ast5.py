from collections import OrderedDict

(INTEGER, REAL, PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV, LPAREN, RPAREN, ID, ASSIGN,
 BEGIN, END, SEMI, DOT, COLON, COMMA, EOF, VAR, PROGRAM) = (
    'INTEGER', 'REAL', 'PLUS', 'MINUS', 'MUL', 'INTEGER_DIV', 'FLOAT_DIV', '(', ')', 'ID', 'ASSIGN',
    'BEGIN', 'END', 'SEMI', 'DOT', 'COLON', 'COMMA', 'EOF', 'VAR', 'PROGRAM'
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
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'VAR': Token('VAR', 'VAR'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
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

    def peek2(self):  # 看再下一个位置而不移动指针
        _peek_pos = self._pos + 2
        if _peek_pos > len(self._text) - 1:
            return None
        else:
            return self._text[_peek_pos]

    def skip_comment(self):
        while self._current_char != '}':
            self.advance()
        self.advance()

    def skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self.advance()

    def number(self):
        _number = ''
        while self._current_char is not None and self._current_char.isdigit():
            _number += self._current_char
            self.advance()

        if self._current_char == '.':
            _number += self._current_char
            self.advance()

            while self._current_char is not None and self._current_char.isdigit():
                _number += self._current_char
                self.advance()
            _token = Token(REAL, float(_number))
        else:
            _token = Token(INTEGER, int(_number))

        return _token

    def _id(self, underscore=False):
        _identifier = '' if not underscore else '_'
        while self._current_char is not None and self._current_char.isalnum():
            _identifier += self._current_char
            self.advance()
        # 因为pascal是大小写不敏感的，所以要转换一下
        _token = RESERVED_KEYWORDS.get(_identifier.upper(), Token(ID, _identifier.upper()))
        # print(_token)
        return _token

    def get_next_token(self):
        while self._current_char is not None:

            if self._current_char.isspace():
                self.skip_whitespace()
                continue

            if self._current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self._current_char == '_' and self.peek().isalpha():
                self.advance()
                return self._id(True)

            if self._current_char.isalpha():
                return self._id()

            if self._current_char.isdigit():
                return self.number()

            if self._current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self._current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self._current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self._current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            # 不需要这一步，因为会在_id方法中处理这个关键字
            # if self._current_char == 'D' and self.peek() == 'I' and self.peek2() == 'V':
            #     self.advance()
            #     self.advance()
            #     self.advance()
            #     return Token(INTEGER_DIV, 'DIV')

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
                return Token(FLOAT_DIV, '/')

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


class Symbol:
    def __init__(self, name, type_=None):
        self.name = name
        self.type = type_

    def __repr__(self):
        return self.__str__()


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name


class VarSymbol(Symbol):
    def __init__(self, name, type_):
        super().__init__(name, type_)

    def __str__(self):
        return '<{name}>: <{type_}>'.format(name=self.name, type_=self.type)


class SymbolTable:
    def __init__(self):
        self._symbols = OrderedDict()
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol(INTEGER))
        self.define(BuiltinTypeSymbol(REAL))

    def __str__(self):
        return 'Symbols: {symbols}'.format(symbols=[value for value in self._symbols.values()])

    def __repr__(self):
        return self.__str__()

    def define(self, symbol):
        print('Define: {}'.format(symbol))
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print('Lookup: {}'.format(name))
        return self._symbols.get(name)


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


class Num(AST):  # 后面用Type代替了
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


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    def __init__(self, lexer):
        self._lexer = lexer
        self._current_token = self._lexer.get_next_token()

    def error(self, msg=None):
        raise Exception('interpreter error {}'.format(msg))

    def eat(self, token_type):  # 处理完当前token，向下走
        if self._current_token.type == token_type:
            self._current_token = self._lexer.get_next_token()
        else:
            self.error(self._current_token)

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
        elif _token.type == REAL:  # 加了浮点数
            self.eat(REAL)
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

        while self._current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            _op = self._current_token
            if _op.value == '*':
                self.eat(MUL)
            elif _op.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif _op.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)

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
        self.eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(DOT)
        return program_node

    def block(self):
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        declarations = []
        if self._current_token.type == VAR:
            self.eat(VAR)
            while self._current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)
        return declarations

    def variable_declaration(self):
        var_nodes = [Var(self._current_token)]
        self.eat(ID)

        while self._current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self._current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec()
        var_declarations = [VarDecl(var_node, type_node) for var_node in var_nodes]

        return var_declarations

    def type_spec(self):
        token = self._current_token
        if self._current_token.type == INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        node = Type(token)
        return node


class NodeVisitor:
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit(self, node):  # 类似适配器，根据不同的method_name去选择不同的方法
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

# 符号表目的是编译时发现一些静态错误，如未声明就调用，类型错误


class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.symbol_table.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symbol_table.define(var_symbol)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))
        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symbol_table.lookup(var_name)

        if var_symbol is None:
            raise NameError(repr(var_name))


class Interpreter(NodeVisitor):
    GLOBAL_SCOPE = {}

    def __init__(self, tree):
        self._tree = tree

    def visit_BinOp(self, node):  # 定义了具体的操作方法
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
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

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def interpret(self):
        # tree = self._parser.parse()  # 拿到的是树的根结点
        if self._tree is None:
            return ''
        return self.visit(self._tree)


if __name__ == '__main__':
    tt = '''\
PROGRAM Part11;
VAR
   number : INTEGER;
   a, b   : INTEGER;
   y      : REAL;

BEGIN {Part11}
   number := 2;
   a := number ;
   b := 10 * a + 10 * number DIV 4;
   y := 20 / 7 + 3.14
END.  {Part11}
'''
    lexer = Lexer(tt)
    parser = Parser(lexer)
    tree = parser.parse()
    symbol_builder = SymbolTableBuilder()
    symbol_builder.visit(tree)
    print('\nSymbol table contents:')
    print(symbol_builder.symbol_table)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)
