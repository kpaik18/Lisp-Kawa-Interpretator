from tokenizer import *
from main_methods import *
from eval_methods import *


def simple_tests(filename):
    with open(filename, 'r') as f:
        all_tests = 0
        passed = 0
        for line in f:
            if line == '\n':
                break
            tokens = line.split('$')
            to_eval = tokens[0]
            tokens_to_eval = tokenize(ready_to_token(to_eval))
            res = make_input_list(tokens_to_eval)
            eval_result = evaluate(res)
            correct_answer = tokens[1]
            print("Evaluating" + to_eval)
            print("Expected: " + correct_answer)
            print(printer(eval_result))
            if str(printer(eval_result)) == correct_answer:
                print('Passed')
                passed = passed + 1
            all_tests = all_tests + 1
            print("")
        print("-----------------------------------------------")
        print("Tested " + str(all_tests) + " TestCases")
        print(str(passed) + " passed")
        print(str(all_tests - passed) + " failed")


def function_tests():
    with open('TestFiles/function_definitions.txt', 'r') as f:
        print("This Test reads functions definitions and checks them")
        for line in f:
            if line == '\n':
                break
            print("Function: " + line)
            tokens_to_eval = tokenize(ready_to_token(line))
            res = make_input_list(tokens_to_eval)
            evaluate(res)
        simple_tests('TestFiles/function_tests.txt')
