from specific_evaluations import *


language_symbols = {'+', '-', '*', '/'}
list_operations = {'car', 'cdr', 'cons', 'append', 'apply', 'length', 'list', 'eval'}
boolean_operators = {'<', '<=', '>', '>=', '='}
list_booleans = {'null?', 'list?'}
conditional_operators = {'if', 'cond', 'and', 'or', 'not'}
define_keywords = {'define'}
map_keywords = {'map'}
function_keywords = set({})
functions = dict()
function_bodies = dict()

important_set = set({})

fill_set(important_set, language_symbols)
fill_set(important_set, list_operations)
fill_set(important_set, boolean_operators)
fill_set(important_set, list_booleans)
fill_set(important_set, conditional_operators)
fill_set(important_set, define_keywords)
fill_set(important_set, map_keywords)


def spec_eval(spec_eval_list):
    special_command = spec_eval_list[1]
    if special_command in language_symbols:
        return symbol_eval(spec_eval_list, special_command)
    if special_command in list_operations:
        return list_eval(spec_eval_list, special_command)
    if special_command in boolean_operators:
        return bool_eval(spec_eval_list)
    if special_command in list_booleans:
        return list_bool_eval(spec_eval_list)
    if special_command in conditional_operators:
        return conditional_eval(spec_eval_list)
    if special_command in define_keywords:
        return define_eval(spec_eval_list)
    if special_command in map_keywords:
        return map_eval(spec_eval_list)


def evaluate(input_to_eval):
    if isinstance(input_to_eval, list):
        if len(input_to_eval) == 1:
            return input_to_eval
        elif not isinstance(input_to_eval[1], list) and input_to_eval[1] in important_set:
            return spec_eval(input_to_eval)
        elif not isinstance(input_to_eval[1], list) and input_to_eval[1] in function_keywords:
            return function_eval(input_to_eval)
        else:
            result = []
            for elem in input_to_eval:
                result.append(evaluate(elem))
            return result
    else:
        try:
            check = float(input_to_eval)
            if float(input_to_eval) == int(float(input_to_eval)):
                return int(input_to_eval)
            else:
                return float(input_to_eval)
        except ValueError:
            return input_to_eval
