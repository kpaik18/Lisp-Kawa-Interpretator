from helper_methods import *


def ready_to_token(input_string):
    out = ""
    for ch in input_string:
        if is_parentheses(ch) > -1:
            out += " " + ch + " "
        else:
            out += ch
    return out


def tokenize(input_string):
    return input_string.split()
