from lexer import *


class Int:
    def __init__(self, token):
        self.value = token.value
        self.op = token.type


class Arr:
    def __init__(self, token):
        self.value = token.value
        self.op = token.type


class Var:
    def __init__(self, token):
        self.value = token.value
        self.op = token.type


class Bool:
    def __init__(self, token):
        self.value = token.value
        self.op = token.type


class Not:
    def __init__(self, node):
        self.op = 'NOT'
        self.ap = node


class BinaryOperation:
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op


class BoolOperation:
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op


class Skip:
    def __init__(self, token):
        self.value = token.value
        self.op = token.type


class Assign:
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op


class Semi:
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op


class While:
    def __init__(self, condition, whiletrue, whilefalse):
        self.condition = condition
        self.whiletrue = whiletrue
        self.whilefalse = whilefalse
        self.op = 'WHILE'


class If:
    def __init__(self, condition, iftrue, iffalse):
        self.condition = condition
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.op = 'IF'


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.state = lexer.state
        self.current_token = lexer.get_next_token()

    def syntax_error(self):
        raise Exception('Invalid input !')

    def factor(self):
        token = self.current_token
        if token.type == 'MINUS':
            self.current_token = self.lexer.get_next_token()
            token = self.current_token
            token.value = -token.value
            node = Int(token)
        elif token.type == 'INT':
            node = Int(token)
        elif token.type == 'VAR':
            node = Var(token)
        elif token.type == 'ARR':
            node = Arr(token)
        elif token.type == 'NOT':
            self.current_token = self.lexer.get_next_token()
            if self.current_token.type == 'LPAREN':
                self.current_token = self.lexer.get_next_token()
                node = self.boolean_expression()
            elif self.current_token.type == 'BOOL':
                node = Bool(self.current_token)
            else:
                self.syntax_error()
            node = Not(node)
        elif token.type == 'BOOL':
            node = Bool(token)
        elif token.type == 'LPAREN':
            self.current_token = self.lexer.get_next_token()
            node = self.boolean_expression()
        elif token.type == 'RPAREN':
            self.current_token = self.lexer.get_next_token()
        elif token.type == 'LBRACE':
            self.current_token = self.lexer.get_next_token()
            node = self.statement_expression()
        elif token.type == 'RBRACE':
            self.current_token = self.lexer.get_next_token()
        elif token.type == 'SKIP':
            node = Skip(token)
        elif token.type == 'WHILE':
            self.current_token = self.lexer.get_next_token()
            condition = self.boolean_expression()
            whilefalse = Skip(Token('SKIP', 'skip'))
            if self.current_token.type == 'DO':
                self.current_token = self.lexer.get_next_token()
                if self.current_token == 'LBRACE':
                    whiletrue = self.statement_expression()
                else:
                    whiletrue = self.statement_term()

            return While(condition, whiletrue, whilefalse)
        elif token.type == 'IF':
            self.current_token = self.lexer.get_next_token()
            condition = self.boolean_expression()
            if self.current_token.type == 'THEN':
                self.current_token = self.lexer.get_next_token()
                iftrue = self.statement_expression()
            if self.current_token.type == 'ELSE':
                self.current_token = self.lexer.get_next_token()
                iffalse = self.statement_expression()
            return If(condition, iftrue, iffalse)
        else:
            self.syntax_error()
        self.current_token = self.lexer.get_next_token()
        return node

    def arith_term(self):
        node = self.factor()
        while self.current_token.type == 'MUL':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left=node, right=self.factor(), op=type_name)
        return node

    def arith_expression(self):
        node = self.arith_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left=node, right=self.arith_term(), op=type_name)
        return node

    def arith_parse(self):
        return self.arith_expression()

    def boolean_term(self):
        node = self.arith_expression()
        if self.current_token.type in ('EQ', 'LS', 'GR'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BoolOperation(left=node, right=self.arith_expression(), op=type_name)
        return node

    def boolean_expression(self):
        node = self.boolean_term()
        while self.current_token.type in ('AND', 'OR'):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinaryOperation(left=node, right=self.boolean_term(), op=type_name)
        return node

    def boolean_parse(self):
        return self.boolean_expression()

    def statement_term(self):
        node = self.boolean_expression()
        if self.current_token.type == 'ASSIGN':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Assign(left=node, right=self.boolean_expression(), op=type_name)
        return node

    def statement_expression(self):
        node = self.statement_term()
        while self.current_token.type == 'SC':
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Semi(left=node, right=self.statement_term(), op=type_name)
        return node

    def statement_parse(self):
        return self.statement_expression()
