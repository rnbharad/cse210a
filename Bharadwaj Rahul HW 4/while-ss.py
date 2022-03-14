#!/usr/bin/python3
from parser import *
from interpreter import *

def main():
    contents = []
    line = input()
    line = line.strip()
    line = ' '.join(line.split())
    contents.append(line)
    user_input = ' '.join(contents)
    user_input = ' '.join(user_input.split())
    lexer = Tokenizer(user_input)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.visit()
    steps = interpreter.print_ss
    steps = [item for sublist in steps for item in sublist]
    states = interpreter.immstate
    if user_input[0:5] == 'skip;' or user_input[0:6] == 'skip ;':
        del steps[0]
        del states[0]
    steps[-1] = 'skip'
    if len(states) > 10000:
        states = states[0:10000]
        steps = steps[0:10000]
    if len(states) == 1 and states[0] == {} and user_input[0:4] == 'skip':
        print('')
    else:
        for i in range(len(states)):
            output_string = []
            for key in sorted(states[i]):
                output_string.append(' '.join([key, '→', str(states[i][key])]))
            state_string = ''.join(['{', ', '.join(output_string), '}'])
            step_string = ' '.join(['⇒', steps[i]])
            print(step_string, state_string, sep=', ')


if __name__ == '__main__':
    main()
