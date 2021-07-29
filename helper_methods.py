def is_parentheses(ch):
    if ch == '(':
        return 1
    elif ch == ')':
        return 0
    else:
        return -1


def check_balance(input_string):
    stack = []
    for ch in input_string:
        res = is_parentheses(ch)
        if res == -1:
            continue
        if res == 1:
            stack.append(ch)
        if res == 0:
            if len(stack) == 0:
                return -1
            stack.pop()
    if len(stack) != 0:
        return 0
    else:
        return 1


def is_number(eval_staff):
    if isinstance(eval_staff, list):
        return False
    elif type(eval_staff) == int or type(eval_staff) == float:
        return True
    else:
        return False


def fill_set(to_fill_set, filler_set):
    for elem in filler_set:
        to_fill_set.add(elem)