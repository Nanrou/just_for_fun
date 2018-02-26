from collections import OrderedDict


INTEGER = 'INTEGER'
REAL = 'REAL'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ID = 'ID'
ASSIGN = 'ASSIGN'
BEGIN = 'BEGIN'
END = 'END'
SEMI = 'SEMI'
DOT = 'DOT'
PROGRAM = 'PROGRAM'
VAR = 'VAR'
COLON = 'COLON'
COMMA = 'COMMA'
EOF = 'EOF'


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type, self.value)

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'VAR': Token('VAR', 'VAR'),
    'DIV': Token('INTEGER_DIV', 'DIV'),  # 在这里处理DIV这个特殊的关键字
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
    'PROCEDURE': Token('PROCEDURE', 'PROCEDURE'),
}


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise RuntimeError()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        _next_pos = self.pos + 1
        if _next_pos < len(self.text):
            return self.text[_next_pos]

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_number(self):
        _num = ''
        while self.current_char is not None and self.current_char.isdigit():
            _num += self.current_char
            self.advance()

        if self.current_char == '.':
            _num += '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                _num += self.current_char
                self.advance()
            return Token(REAL_CONST, float(_num))

        return Token(INTEGER_CONST, int(_num))

    def get_variable(self):
        _identifier = ''
        while self.current_char is not None and self.current_char.isalnum():
            _identifier += self.current_char
            self.advance()
        return RESERVED_KEYWORDS.get(_identifier.upper(), Token(ID, _identifier.upper()))  # 这里就是捕获变量这个字面值的地方

    def get_next_token(self):
        while self.current_char is not None:

            # 跳过
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.skip_comment()
                continue

            # 取值
            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char.isalpha() or self.current_char == '_':  # 变量由数字字母组合，但不可以是数字开头
                return self.get_variable()

            # 非操作符
            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            # 操作符
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

        return Token(EOF, None)


class Symbol:
    def __init__(self, name, type_=None):
        self.name = name
        self.type = type_


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class VarSymbol(Symbol):
    def __init__(self, name, type_):
        super().__init__(name, type_)

    def __str__(self):
        return '<{name}: {type_}>'.format(name=self.name, type_=self.type)

    def __repr__(self):
        return self.__str__()


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


class UnaryOp(AST):  # 一元操作符
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class BinOp(AST):  # 二元操作符
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


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


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


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg=None):
        raise RuntimeError('parser error {}'.format(msg))

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()  # 这里就往前走了，就像lexer中的advance
        else:
            self.error('{} with {}'.format(self.current_token, token_type))

    def factor(self):  # unary_op factor | num | ( expr ) | variable
        _token = self.current_token

        if _token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(_token, self.factor())
        elif _token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(_token, self.factor())

        if _token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(_token)
        elif _token.type == REAL_CONST:
            self.eat(REAL_CONST)
            return Num(_token)
        elif _token.type == LPAREN:
            self.eat(LPAREN)
            _node = self.expr()
            self.eat(RPAREN)
            return _node

        return self.variable()

    def term(self):
        _node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            _op = self.current_token
            if _op.type == MUL:
                self.eat(MUL)
            elif _op.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif _op.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)

            _node = BinOp(_node, _op, self.factor())  # term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
        return _node

    def expr(self):
        _node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            _op = self.current_token
            if _op.type == PLUS:
                self.eat(PLUS)
            elif _op.type == MINUS:
                self.eat(MINUS)

            _node = BinOp(_node, _op, self.term())  # expr : term ((PLUS | MINUS) term)*
        return _node

    def variable(self):
        _node = Var(self.current_token)
        self.eat(ID)
        return _node

    def type_spec(self):
        _token = self.current_token
        if _token.type == INTEGER:
            self.eat(INTEGER)
        elif _token.type == REAL:
            self.eat(REAL)
        return Type(_token)

    @staticmethod
    def empty():
        return NoOp()

    def assignment_statement(self):  # variable := expr
        _left = self.variable()
        _token = self.current_token
        self.eat(ASSIGN)
        _right = self.expr()
        return Assign(_left, _token, _right)  # op也就是个:=

    def statement(self):  # compound_statement | assignment_statement | empty
        if self.current_token.type == BEGIN:
            return self.compound_statement()
        elif self.current_token.type == ID:
            return self.assignment_statement()
        else:
            return self.empty()

    def statement_list(self):  # statement (SEMI statement)* (SEMI)?
        _statement_list_node = [self.statement()]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            _statement_list_node.append(self.statement())

        if self.current_token == ID:
            self.error()

        return _statement_list_node

    def compound_statement(self):  # BEGIN statement_list END
        self.eat(BEGIN)
        _child_list = self.statement_list()
        self.eat(END)

        _compound_node = Compound()
        for child in _child_list:
            _compound_node.children.append(child)
        return _compound_node

    def variable_declaration(self):  # A,B,C:REAL
        variables = [Var(self.current_token)]
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            variables.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec()
        var_declarations = [VarDecl(variable, type_node) for variable in variables]

        return var_declarations

    def declarations(self):  # VAR (variable_declaration)+ | empty
        _declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_declarations = self.variable_declaration()
                _declarations.extend(var_declarations)
                self.eat(SEMI)
        return _declarations

    def block(self):  # declarations compound_statement
        return Block(self.declarations(), self.compound_statement())

    def program(self):  # PROGRAM variable SEMI block DOT
        self.eat(PROGRAM)
        program_name = self.variable().value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(program_name, block_node)
        self.eat(DOT)
        return program_node

    def parser(self):
        return self.program()


class NodeVisitor:
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit(self, node):  # 反射，根据结点去找对应的处理方法
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_program(self, node):
        self.visit(node.block)

    def visit_block(self, node):
        for declaration in node.declarations:  # 声明部分，确定变量的类型
            self.visit(declaration)
        self.visit(node.compound_statement)  # 逻辑部分，确定变量已经声明

    def visit_compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_vardecl(self, node):  # 生成变量和类型的对应关系，储存在symbol表中
        type_name = node.type_node.value
        type_symbol = self.symbol_table.lookup(type_name)  # 拿到标准类型
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symbol_table.define(var_symbol)

    def visit_binop(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_unaryop(self, node):
        self.visit(node.expr)

    def visit_assign(self, node):  # x := expr;
        var_name = node.left.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))
        self.visit(node.right)

    def visit_var(self, node):  # 确保变量已经声明了
        var_name = node.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))

    def visit_num(self, node):
        pass

    def visit_noop(self, node):
        pass


class Interpreter(NodeVisitor):  # 这里才是真正操作执行

    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = OrderedDict()

    # 基础逻辑部分
    def visit_num(self, node):
        return node.value

    def visit_binop(self, node):
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

    def visit_unaryop(self, node):
        if node.op.type == PLUS:
            return +self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr)

    def visit_noop(self, node):
        pass

    # 普通语句部分
    def visit_var(self, node):
        return self.GLOBAL_SCOPE.get(node.value)

    def visit_assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_compound(self, node):
        for child in node.children:
            self.visit(child)

    # 声明部分，暂时用不到这部分
    def visit_vardecl(self, node):
        print('var declaration state -- ', node)

    def visit_type(self, node):
        print('type state -- ', node)

    def visit_block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_program(self, node):
        self.visit(node.block)

    def interpreter(self):
        _tree = self.parser.parser()
        return self.visit(_tree)


if __name__ == '__main__':
    ss = '1 + (-2) - 3 * 4 / (5 + 6)'

    tt = '''\
PROGRAM Part10;
VAR
   number     : INTEGER;
   a, b, c, x : INTEGER;
   y          : REAL;

BEGIN {Part10}
   BEGIN
      number := 2;
      a := number;
      b := 10 * a + 10 * number DIV 4;
      c := a - - b
   END;
   x := 11;
   y := 20 / 7 + 3.14;
   { writeln('a = ', a); }
   { writeln('b = ', b); }
   { writeln('c = ', c); }
   { writeln('number = ', number); }
   { writeln('x = ', x); }
   { writeln('y = ', y); }
END. {Part10}
'''
    dd = """\
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

"""

    # ll = Lexer(tt)
    ll = Lexer(dd)
    pp = Parser(ll)
    sy = SymbolTableBuilder()
    sy.visit(pp.parser())
    print(sy.symbol_table)

    ll = Lexer(dd)
    pp = Parser(ll)
    ii = Interpreter(pp)
    ii.interpreter()
    print(ii.GLOBAL_SCOPE)
