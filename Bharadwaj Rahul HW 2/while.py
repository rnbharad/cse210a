from parser import *
from interpreter import *


def main():
    line = [input()]
    text = ' '.join(line)
    lexer = Tokenizer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.visit()
    state_list = interpreter.immediate_state

    if text == 'skip;':
        del state_list
    else:
        for i in range(len(state_list)):
            x = []
            for key in sorted(state_list[i]):
                x.append(' '.join([key, '→', str(state_list[i][key])]))
        result = ''.join(['{', ', '.join(x), '}'])
    print(result)


if __name__ == '__main__':
    main()
