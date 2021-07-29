from tokenizer import *
from main_methods import *
from eval_methods import *


inp = ""
while True:
    inp += input("kawa: ")
    if inp == "(exit)":
        break
    if check_balance(inp) == -1:
        print("parentheses cant be balanced")
        inp = ""
    elif check_balance(inp) == 0:
        continue
    elif check_balance(inp) == 1:
        # tokens input
        tokens = tokenize(ready_to_token(inp))
        # makes list from tokens
        res = make_input_list(tokens)
        # evaluating results
        eval_result = evaluate(res)
        # to print kawa ready interpretation, must change to printing evaluate results
        print(printer(eval_result))
        inp = ""
