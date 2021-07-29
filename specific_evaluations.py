import eval_methods as ev
from helper_methods import *


true = '#t'
false = '#f'
NULL = 'not_some_random_word'


def search_in_array(to_find, array):
    i = 0
    while i < len(array):
        if to_find == array[i]:
            return i
        i = i + 1
    return -1


def change_all_occurences(to_change, to_search, real_args):
    result = []
    counter = 0
    while counter < len(to_change):
        elem = to_change[counter]
        if isinstance(elem, list):
            result.append(change_all_occurences(elem, to_search, real_args))
        else:
            find = search_in_array(elem, to_search)
            if find != -1:
                result.append(real_args[find])
            else:
                result.append(elem)
        counter = counter + 1
    return result


def change_body(body, search, final):
    result = []
    for elem in body:
        if isinstance(elem, list):
            result.append(change_body(elem, search, final))
        else:
            if elem == search:
                result.append(final)
            else:
                result.append(ev.evaluate(elem))
    return result


def lambda_eval(spec_eval_list):
    lambda_definition = spec_eval_list[2]
    list_to_map = ev.evaluate(spec_eval_list[3])
    if len(lambda_definition) < 4:
        print("lambda syntax is wrong")
    else:
        arg_list = lambda_definition[2]
        if not isinstance(arg_list, list):
            print("lambda syntax is wrong")
        else:
            if len(arg_list) != 2:
                print("lambda syntax is wrong")
            else:
                arg_name = arg_list[1]
                lambda_body = lambda_definition[3:]
                counter = 1
                tmp_body = lambda_body
                result = [' ']
                while counter < len(list_to_map):
                    tmp_body = change_body(tmp_body, arg_name, list_to_map[counter])
                    if len(tmp_body) == 1:
                        tmp_body = tmp_body[0]
                    else:
                        tmp_body.insert(0, ' ')
                    counter = counter + 1
                    result.append(tmp_body)
                    tmp_body = lambda_body
                return ev.evaluate(result)


def map_eval(spec_eval_list):
    if len(spec_eval_list) != 4:
        print('map take two arguments, function and list')
    else:
        function_name = spec_eval_list[2]
        if isinstance(function_name, list):
            if function_name[1] == 'lambda':
                return lambda_eval(spec_eval_list)
            else:
                print('not valid function or lambda')
        elif function_name in ev.function_keywords:
            list_to_map = ev.evaluate(spec_eval_list[3])
            if not isinstance(list_to_map, list):
                print('second argument must be list')
            else:
                result = [' ']
                counter = 1
                while counter < len(list_to_map):
                    function_to_eval = [' ', function_name, list_to_map[counter]]
                    result.append(function_eval(function_to_eval))
                    counter = counter + 1
                return result
        else:
            print("not valid function name")


def function_eval(spec_eval_list):
    function_name = spec_eval_list[1]
    saved_arguments = ev.functions[function_name]
    if saved_arguments == NULL:
        if len(spec_eval_list) != 2:
            print("can't be evaluated")
        else:
            return ev.evaluate(ev.function_bodies[function_name])
    else:
        arg_count = len(saved_arguments)
        if len(spec_eval_list) != arg_count + 2:
            print("function can't be evaluated, not correct number of arguments")
        else:
            temp_arguments = []
            counter = 0
            while counter < arg_count:
                temp_arguments.append(ev.evaluate(spec_eval_list[2 + counter]))
                counter = counter + 1
            function_body = ev.function_bodies[function_name]
            i = 0
            function_argument_names = ev.functions[function_name]
            function_body = change_all_occurences(function_body, function_argument_names, temp_arguments)
            return ev.evaluate(function_body)


def define_eval(spec_eval_list):
    if len(spec_eval_list) != 4:
        print('function cant be created')
    else:
        function_staff = spec_eval_list[2]
        if not isinstance(function_staff, list):
            print('this function cant be evaluated')
            return
        new_function_name = function_staff[1]
        if new_function_name in ev.important_set:
            print("function with that name can't be defined ")
        else:
            ev.function_keywords.add(new_function_name)
            if len(function_staff) == 2:
                ev.functions[new_function_name] = NULL
            else:
                argument_names = []
                counter = 2
                while counter < len(function_staff):
                    argument_names.append(function_staff[counter])
                    counter = counter + 1
                ev.functions[new_function_name] = argument_names
            ev.function_bodies[new_function_name] = spec_eval_list[3]


def check_cond(cond_list):
    if len(cond_list) != 3:
        print("cond syntax error")
        return False
    else:
        if ev.evaluate(cond_list[1]) == true:
            return True
        elif ev.evaluate(cond_list[1]) == false:
            return False
        elif ev.evaluate(cond_list[1]) == 'else':
            return True
        else:
            print('cond expression cant be evaluated')


def is_valid_boolean(check):
    if check == true or check == false:
        return True
    return False


def and_eval(first, second):
    if first == true and second == true:
        return true
    return false


def or_eval(first, second):
    if first == true or second == true:
        return true
    return false


def conditional_eval(spec_eval_list):
    cond_symbol = spec_eval_list[1]
    if cond_symbol == 'if':
        if len(spec_eval_list) != 5:
            print('if needs boolean expression, and two arguments')
        else:
            bool_arg = ev.evaluate(spec_eval_list[2])
            if bool_arg == true:
                return ev.evaluate(spec_eval_list[3])
            elif bool_arg == false:
                return ev.evaluate(spec_eval_list[4])
            else:
                print("first argument must be true or false")
    if cond_symbol == 'cond':
        if len(spec_eval_list) < 3:
            print("cond cant be evaluated without arguments")
        else:
            size_of_list = len(spec_eval_list)
            last_conditional = spec_eval_list[size_of_list - 1]
            if last_conditional[1] != 'else':
                print("invalid use of else")
            else:
                counter = 2
                while counter < size_of_list :
                    to_eval_list = spec_eval_list[counter]
                    if check_cond(to_eval_list):
                        return ev.evaluate(to_eval_list[2])
                    counter = counter + 1
    if cond_symbol == 'and' or cond_symbol == 'or':
        if len(spec_eval_list) != 4:
            print('and needs two arguments')
        else:
            first_arg = ev.evaluate(spec_eval_list[2])
            if not is_valid_boolean(first_arg):
                print("first argument doesn't evaluate to boolean")
            else:
                second_arg = ev.evaluate(spec_eval_list[3])
                if not is_valid_boolean(second_arg):
                    print("second argument doesn't evaluate to boolean")
                else:
                    if cond_symbol == 'and':
                        return and_eval(first_arg, second_arg)
                    if cond_symbol == 'or':
                        return or_eval(first_arg, second_arg)
    if cond_symbol == 'not':
        if len(spec_eval_list) != 3:
            print('not must take only one argument')
        else:
            bool_arg = ev.evaluate(spec_eval_list[2])
            if is_valid_boolean(bool_arg):
                if bool_arg == true:
                    return false
                else:
                    return true
            else:
                print('argument is not valid boolean')


def list_bool_eval(spec_eval_list):
    list_boolean_operator = spec_eval_list[1]
    if list_boolean_operator == 'null?':
        if len(spec_eval_list) != 3:
            print('null? must take one list argument')
        else:
            list_to_eval = ev.evaluate(spec_eval_list[2])
            if not isinstance(list_to_eval, list):
                print('null? must evaluate list')
            else:
                if len(list_to_eval) > 1:
                    return false
                else:
                    return true
    if list_boolean_operator == 'list?':
        if len(spec_eval_list) != 3:
            print('list? must take one argument')
        else:
            list_to_eval = ev.evaluate(spec_eval_list[2])
            if isinstance(list_to_eval, list):
                return true
            else:
                return false


def bool_symbol_eval(first_num, second_num, bool_symbol):
    if bool_symbol == '=':
        if first_num == second_num:
            return true
        else:
            return false
    if bool_symbol == '<':
        if first_num < second_num:
            return true
        else:
            return false
    if bool_symbol == '<=':
        if first_num <= second_num:
            return true
        else:
            return false
    if bool_symbol == '>':
        if first_num > second_num:
            return true
        else:
            return false
    if bool_symbol == '>=':
        if first_num >= second_num:
            return true
        else:
            return false


def bool_eval(spec_eval_list):
    bool_symbol = spec_eval_list[1]
    if len(spec_eval_list) == 2:
        print("need arguments to evaluate " + bool_symbol)
    else:
        if len(spec_eval_list) != 4:
            print(bool_symbol + " evaluation needs exactly two arguments")
        else:
            first_num = ev.evaluate(spec_eval_list[2])
            second_num = ev.evaluate(spec_eval_list[3])
            try:
                check1 = float(first_num)
                check2 = float(second_num)
                return bool_symbol_eval(first_num, second_num, bool_symbol)
            except ValueError:
                print('arguments must be numbers')


def list_eval(spec_eval_list, special_command):
    # car evaluation
    if special_command == 'car':
        if len(spec_eval_list) == 2:
            print("cannot invoke car without arguments")
        elif len(spec_eval_list) > 3:
            print("cannot invoke car on many lists")
        elif not isinstance(spec_eval_list[2], list):
            print("car must be invoked on a list")
        else:
            tmp = ev.evaluate(spec_eval_list[2])
            if not isinstance(tmp, list):
                print("car must be invoked on a list")
            elif len(tmp) < 2:
                print("car must not be invoked on empty list")
            else:
                return tmp[1]
    # cdr evaluation
    if special_command == 'cdr':
        if len(spec_eval_list) == 2:
            print('cdr cannot be invoked without arguments')
        elif len(spec_eval_list) > 3:
            print("cannot invoke cdr on many lists")
        elif not isinstance(spec_eval_list[2], list):
            print("cdr must be invoked on a list")
        else:
            tmp = ev.evaluate(spec_eval_list[2])
            if not isinstance(tmp, list):
                print("cdr must be invoked on a list")
            elif len(tmp) < 2:
                print("to invoke cdr, list must have minimum 1 elements")
            else:
                result = tmp[2:]
                result.insert(0, ' ')
                return result
    # cons evaluation
    if special_command == 'cons':
        if len(spec_eval_list) == 2:
            print('cons cant be invoked without arguments')
        elif len(spec_eval_list) != 4:
            print('cons need exactly two arguments')
        else:
            destination = ev.evaluate(spec_eval_list[3])
            if not isinstance(destination, list):
                print('second argument must be the list')
            else:
                to_add = ev.evaluate(spec_eval_list[2])
                destination.insert(1, to_add)
                return destination
    # append evaluation
    if special_command == 'append':
        if len(spec_eval_list) == 2:
            print('append cant be invoked without arguments')
        elif len(spec_eval_list) != 4:
            print('append must work on 2 arguments')
        else:
            first_list = ev.evaluate(spec_eval_list[2])
            if not isinstance(first_list, list):
                print('first argument must be the list')
            else:
                second_list = ev.evaluate(spec_eval_list[3])
                if not isinstance(second_list, list):
                    print('second argument must be the list')
                else:
                    second_counter = 1
                    while second_counter < len(second_list):
                        first_list.append(second_list[second_counter])
                        second_counter = second_counter + 1
                    return first_list
    # apply evaluation
    if special_command == 'apply':
        if len(spec_eval_list) == 2:
            print("apply can't be invoked without arguments")
        elif len(spec_eval_list) != 4:
            print('apply needs exactly two arguments')
        else:
            if spec_eval_list[2] not in ev.language_symbols:
                print('first argument of apply needs to be a symbol')
            else:
                to_apply_list = ev.evaluate(spec_eval_list[3])
                if not isinstance(to_apply_list, list):
                    print('apply must be invoked on a list')
                else:
                    to_apply_list.insert(1, spec_eval_list[2])
                    return symbol_eval(to_apply_list, spec_eval_list[2])
    # len evaluation
    if special_command == 'length':
        if len(spec_eval_list) == 2:
            print("length function can't be invoked without arguments")
        elif len(spec_eval_list) != 3:
            print("length function can get one list as an argument")
        else:
            tmp_list = ev.evaluate(spec_eval_list[2])
            if not isinstance(tmp_list, list):
                print("length function must be invoked on a list")
            else:
                return len(tmp_list) - 1
    # list evaluation
    if special_command == 'list':
        if len(spec_eval_list) == 2:
            print("list function can't be invoked without arguments")
        elif len(spec_eval_list) > 3:
            print('list function can be invoked only with one argument')
        else:
            to_list = ev.evaluate(spec_eval_list[2])
            result_list = [' ', to_list]
            return result_list
    if special_command == 'eval':
        if len(spec_eval_list) == 2:
            print("eval can't be invoked without arguments")
        elif len(spec_eval_list) > 3:
            print("eval must be invoked only with one argument")
        else:
            to_list = ev.evaluate(spec_eval_list[2])
            return ev.evaluate(to_list)


def calculate(old_calculation, new_value, spec_symbol):
    if spec_symbol == '+':
        return old_calculation + new_value
    elif spec_symbol == '*':
        return old_calculation * new_value
    elif spec_symbol == '-':
        return old_calculation - new_value
    elif spec_symbol == '/':
        return old_calculation / new_value


def symbol_eval(spec_eval_list, special_symbol):
    if len(spec_eval_list) == 2:
        print("+ can't be evaluated without arguments")
    else:
        result_of_list = ev.evaluate(spec_eval_list[2])
        if not is_number(result_of_list):
            print("cannot apply " + special_symbol + " symbol to not number types")
        eval_counter = 3
        while eval_counter < len(spec_eval_list):
            eval_num = ev.evaluate(spec_eval_list[eval_counter])
            if not is_number(eval_num):
                print("cannot apply " + special_symbol + " symbol to not number types")
            else:
                result_of_list = calculate(result_of_list, eval_num, special_symbol)
            eval_counter = eval_counter + 1
        return result_of_list

