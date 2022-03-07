import copy


class Interpreter:
    def __init__(self, parser):
        self.state = parser.state
        self.ast = parser.statement_parse()
        self.variables = []
        self.immediate_state = []

    def visit(self):
        return eval(self.ast, self.state, self.variables, self.immediate_state)


def dictionary(var, value):
    return dict([tuple([var, value])])


def eval(ast, state, variables, immediate_state):

    state = state
    node = ast
    variables = variables
    immediate_state = immediate_state

    if node.operand in ('INTEGER', 'ARR', 'BOOL'):
        return node.value

    elif node.operand == 'PLUS':
        return eval(node.left, state, variables, immediate_state) + eval(node.right, state, variables, immediate_state)

    elif node.operand == 'MINUS':
        return eval(node.left, state, variables, immediate_state) - eval(node.right, state, variables, immediate_state)

    elif node.operand == 'MUL':
        return eval(node.left, state, variables, immediate_state) * eval(node.right, state, variables, immediate_state)

    elif node.operand == 'NOT':
        return not eval(node.nt, state, variables, immediate_state)

    elif node.operand == 'EQUAL':
        return eval(node.left, state, variables, immediate_state) == eval(node.right, state, variables, immediate_state)

    elif node.operand == 'LS':
        return eval(node.left, state, variables, immediate_state) < eval(node.right, state, variables, immediate_state)

    elif node.operand == 'GR':
        return eval(node.left, state, variables, immediate_state) > eval(node.right, state, variables, immediate_state)

    elif node.operand == 'AND':
        return eval(node.left, state, variables, immediate_state) and eval(node.right, state, variables, immediate_state)

    elif node.operand == 'OR':
        return eval(node.left, state, variables, immediate_state) or eval(node.right, state, variables, immediate_state)

    elif node.operand == 'VAR':
        if node.value in state:
            return state[node.value]
        else:
            return 0

    elif node.operand == 'SKIP':
        state = state
        var1 = set(variables)
        state1 = copy.deepcopy(state)
        state1 = dict((var, state1[var]) for var in var1)
        immediate_state.append(state1)

    elif node.operand == 'SC':
        eval(node.left, state, variables, immediate_state)
        var1 = set(variables)
        state1 = copy.deepcopy(state)
        state1 = dict((var, state1[var]) for var in var1)
        immediate_state.append(state1)
        eval(node.right, state, variables, immediate_state)

    elif node.operand == 'ASSIGN':
        var = node.left.value
        variables.append(var)

        if var in state:
            state[var] = eval(node.right, state, variables, immediate_state)

        else:
            state.update(dictionary(var, eval(node.right, state, variables, immediate_state)))
        var1 = set(variables)
        state1 = copy.deepcopy(state)
        state1 = dict((var, state1[var]) for var in var1)
        immediate_state.append(state1)

    elif node.operand == 'WHILE':
        condition = node.condition
        while_true = node.while_true

        while eval(condition, state, variables, immediate_state):
            var1 = set(variables)
            state1 = copy.deepcopy(state)
            state1 = dict((var, state1[var]) for var in var1)
            immediate_state.append(state1)
            eval(while_true, state, variables, immediate_state)
            var1 = set(variables)
            state1 = copy.deepcopy(state)
            state1 = dict((var, state1[var]) for var in var1)
            immediate_state.append(state1)
        var1 = set(variables)
        state1 = copy.deepcopy(state)
        state1 = dict((var, state1[var]) for var in var1)
        immediate_state.append(state1)

    elif node.operand == 'IF':
        condition = node.condition
        iftrue = node.iftrue
        iffalse = node.iffalse

        if eval(condition, state, variables, immediate_state):
            var1 = set(variables)
            state1 = copy.deepcopy(state)
            state1 = dict((var, state1[var]) for var in var1)
            immediate_state.append(state1)
            eval(iftrue, state, variables, immediate_state)

        else:
            var1 = set(variables)
            state1 = copy.deepcopy(state)
            state1 = dict((var, state1[var]) for var in var1)
            immediate_state.append(state1)
            eval(iffalse, state, variables, immediate_state)

    else:
        raise Exception("Error")


def to_print(node):
    if node.operand in ('INTEGER', 'ARR', 'VAR', 'SKIP'):
        return node.value
    elif node.operand in 'BOOL':
        return str(node.value).lower()
    elif node.operand in ('PLUS', 'MINUS', 'MUL', 'EQUAL', 'SC', 'AND', 'OR'):
        return ''.join(['(', str(to_print(node.left)), node.operand, str(to_print(node.right)), ')'])
    elif node.operand in 'NOT':
        return ''.join([node.operand, str(to_print(node.nt))])
    elif node.operand in 'ASSIGN':
        return ' '.join([str(to_print(node.left)), node.operand, str(to_print(node.right))])
    elif node.operand in 'SC':
        return ' '.join([''.join([str(to_print(node.left)), node.operand]), str(to_print(node.right))])
    elif node.operand in 'WHILE':
        return ' '.join(['while', str(to_print(node.condition)), 'do', '{', str(to_print(node.while_true)), '}'])
    elif node.operand in 'IF':
        return ' '.join(['if', str(to_print(node.condition)), 'then', '{', str(to_print(node.iftrue)), '}', 'else', '{', str(to_print(node.iffalse)), '}'])
    else:
        raise Exception('Syntax Error')
