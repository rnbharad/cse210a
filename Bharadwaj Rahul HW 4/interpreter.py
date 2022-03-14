import copy


def dictionary(var, value):
    return dict( [ tuple( [var, value] ) ] )


def to_print(node):
    if node.op in ('INT', 'ARR', 'VAR', 'SKIP'):
        return node.value
    elif node.op in 'BOOL':
        return str(node.value).lower()
    elif node.op in ('PLUS', 'MINUS', 'MUL', 'EQ', 'LS', 'GR', 'AND', 'OR'):
        return ''.join(['(', str(to_print(node.left)), definitions(node.op), str(to_print(node.right)), ')'])
    elif node.op in 'NOT':
        return ''.join([definitions(node.op), str(to_print(node.ap))])
    elif node.op in 'ASSIGN':
        return ' '.join([str(to_print(node.left)), definitions(node.op), str(to_print(node.right))])
    elif node.op in 'SC':
        return ' '.join([''.join([str(to_print(node.left)), definitions(node.op)]), str(to_print(node.right))])
    elif node.op in 'WHILE':
        return ' '.join(['while', str(to_print(node.condition)), 'do', '{', str(to_print(node.whiletrue)), '}'])
    elif node.op in 'IF':
        return ' '.join(['if', str(to_print(node.condition)), 'then', '{', str(to_print(node.iftrue)), '}', 'else', '{', str(to_print(node.iffalse)), '}'])
    else:
        raise Exception('Syntax Error')


class SubString:
    def __init__(self, string):
        self.string = string

    def __sub__(self, other):
        return self.string.replace(other.string, '', 1)


def eval(ast, state, variables, immstate, print_ss, first_step):
    state = state
    node = ast
    variables = variables
    immstate = immstate
    print_ss = print_ss
    first_step = first_step
    if node.op in ('INT', 'ARR', 'BOOL'):
        return node.value
    elif node.op == 'VAR':
        if node.value in state:
            return state[node.value]
        else:
            state.update(dictionary(node.value, 0))
            return 0
    elif node.op == 'SKIP':
        state = state
        var1 = set(variables)
        state1 = copy.deepcopy(state)
        state1 = dict((var, state1[var]) for var in var1)
        immstate.append(state1)
        step1 = SubString(str(to_print(node)))
        print_ss.append([SubString(SubString(first_step) - step1) - SubString('; ')])
        SubString(SubString(first_step) - step1) - SubString('; ')
    elif node.op == 'SC':
        eval(node.left, state, variables, immstate, print_ss, first_step)
        var1 = set(variables)
        state1 = copy.deepcopy(state)
        state1 = dict((var, state1[var]) for var in var1)
        immstate.append(state1)
        step1 = SubString(str(to_print(node.left)))
        print_ss.append([str(SubString(SubString(first_step) - step1) - SubString('; '))])
        first_step = SubString(SubString(first_step) - step1) - SubString('; ')
        eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'ASSIGN':
        var = node.left.value
        variables.append(var)
        if var in state:
            state[var] = eval(node.right, state, variables, immstate, print_ss, first_step)
        else:
            state.update(dictionary(var, eval(node.right, state, variables, immstate, print_ss, first_step)))
        var1 = set(variables)
        state1 = copy.deepcopy(state)
        state1 = dict((var, state1[var]) for var in var1)
        immstate.append(state1)
        step1 = SubString(str(to_print(node)))
        print_ss.append(['skip; ' + str(SubString(SubString(first_step) - step1) - SubString('; '))])
        SubString(SubString(first_step) - step1) - SubString('; ')

    elif node.op == 'PLUS':
        return eval(node.left, state, variables, immstate, print_ss, first_step) + eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'MINUS':
        return eval(node.left, state, variables, immstate, print_ss, first_step) - eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'MUL':
        return eval(node.left, state, variables, immstate, print_ss, first_step) * eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'NOT':
        return not eval(node.ap, state, variables, immstate, print_ss, first_step)
    elif node.op == 'EQ':
        return eval(node.left, state, variables, immstate, print_ss, first_step) == eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'LS':
        return eval(node.left, state, variables, immstate, print_ss, first_step) < eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'GR':
        return eval(node.left, state, variables, immstate, print_ss, first_step) > eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'AND':
        return eval(node.left, state, variables, immstate, print_ss, first_step) and eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'OR':
        return eval(node.left, state, variables, immstate, print_ss, first_step) or eval(node.right, state, variables, immstate, print_ss, first_step)
    elif node.op == 'WHILE':
        condition = node.condition
        whiletrue = node.whiletrue
        node.whilefalse
        break_while = 0
        while eval(condition, state, variables, immstate, print_ss, first_step):
            break_while += 1
            if break_while >= 10000:
                break
            var1 = set(variables)
            state1 = copy.deepcopy(state)
            state1 = dict((var, state1[var]) for var in var1)
            immstate.append(state1)
            first_step = first_step.replace(to_print(node), str(to_print(node.whiletrue) + '; ' + to_print(node)))
            print_ss.append([first_step])
            eval(whiletrue, state, variables, immstate, print_ss, first_step)
            var1 = set(variables)
            state1 = copy.deepcopy(state)
            state1 = dict((var, state1[var]) for var in var1)
            immstate.append(state1)
            step1 = SubString(str(to_print(node.whiletrue)))
            print_ss.append([SubString(SubString(first_step) - step1) - SubString('; ')])
            first_step = SubString(SubString(first_step) - step1) - SubString('; ')
        var1 = set(variables)
        state1 = copy.deepcopy(state)
        state1 = dict((var, state1[var]) for var in var1)
        immstate.append(state1)
        step1 = SubString(to_print(node))
        print_ss.append(['skip; ' + (SubString(SubString(first_step) - step1) - SubString('; '))])
        SubString(SubString(first_step) - step1) - SubString('; ')
    elif node.op == 'IF':
        condition = node.condition
        iftrue = node.iftrue
        iffalse = node.iffalse
        if eval(condition, state, variables, immstate, print_ss, first_step):
            var1 = set(variables)
            state1 = copy.deepcopy(state)
            state1 = dict((var, state1[var]) for var in var1)
            immstate.append(state1)
            step1 = SubString(str(to_print(node)))
            print_ss.append([str(to_print(node.iftrue)) + (SubString(first_step) - step1)])
            first_step = str(to_print(node.iftrue)) + (SubString(first_step) - step1)
            eval(iftrue, state, variables, immstate, print_ss, first_step)
        else:
            var1 = set(variables)
            state1 = copy.deepcopy(state)
            state1 = dict((var, state1[var]) for var in var1)
            immstate.append(state1)
            step1 = SubString(str(to_print(node)))
            print_ss.append([str(to_print(node.iffalse)) + (SubString(first_step) - step1)])
            first_step = str(to_print(node.iffalse)) + (SubString(first_step) - step1)
            eval(iffalse, state, variables, immstate, print_ss, first_step)
    else:
        raise Exception('Error')


class Interpreter:
    def __init__(self, parser):
        self.state = parser.state
        self.ast = parser.statement_parse()
        self.variables = []
        self.immstate = []
        self.print_ss = []
        self.first_step = to_print(self.ast)

    def visit(self):
        return eval(self.ast, self.state, self.variables, self.immstate, self.print_ss, self.first_step)


def definitions(operand):
    cases = {
        'PLUS': '+',
        'MINUS': '-',
        'MUL': '*',
        'EQ': '=',
        'LS': '<',
        'GR': '>',
        'AND': '∨',
        'OR': '∧',
        'ASSIGN': ':=',
        'SC': ';',
        'NOT': '¬',
    }
    return cases.get(operand, 'Error')
