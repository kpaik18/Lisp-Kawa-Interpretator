def list_sizer(inp_list):
    count = 0
    for elem in inp_list:
        if isinstance(elem, list):
            count = count + list_sizer(elem)
        else:
            count = count + 1
    return count + 1


def make_input_list(input_tokens):
    res = []
    if input_tokens[0] != '(':
        if len(input_tokens) > 1:
            print("invalid token exception - a list type expression cant start without '('")
        else:
            res.append(input_tokens[0])
            return res
    else:
        res.append(' ')
        token_counter = 1
        while token_counter < len(input_tokens):
            if input_tokens[token_counter] == '(':
                tmp = make_input_list(input_tokens[token_counter:])
                res.append(tmp)
                token_counter = token_counter + list_sizer(tmp)
            elif input_tokens[token_counter] == ')':
                return res
            else:
                res.append(input_tokens[token_counter])
                token_counter = token_counter + 1


def printer(listed_input):
    if not isinstance(listed_input, list):
        return listed_input
    if len(listed_input) == 1:
        if listed_input[0] == ' ':
            return '()'
        else:
            return str(listed_input[0])
    else:
        res_str = '('
        counter = 0
        while counter < len(listed_input):
            elem = listed_input[counter]
            if isinstance(elem, list):
                res_str = res_str + printer(elem)
            elif elem == ' ':
                counter = counter + 1
                continue
            else:
                res_str = res_str + str(elem)
            if counter > 0 and counter != len(listed_input) - 1:
                res_str = res_str + ' '
            counter = counter + 1
        res_str = res_str + ')'
    return res_str


