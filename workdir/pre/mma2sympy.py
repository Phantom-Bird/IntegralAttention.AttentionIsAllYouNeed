from sympy import *
from sympy.abc import *
from solution import CONSTANT_TERM_KEY


def add_multiplication(expression):
    import re
    # 使用正则表达式在符合要求的空格位置添加乘号
    expression = re.sub(r'(\d)\s+([a-zA-Z(])', r'\1 * \2', expression)  # 数字-字母或数字-括号
    expression = re.sub(r'([a-zA-Z)])\s+([a-zA-Z(])', r'\1 * \2', expression)  # 字母-字母或括号-字母
    return expression

def convert(expression: str):
    li = [
        (r'\[Pi]', 'pi'),
        ('[', '('),
        (']', ')'),
        ('{', '['),
        ('}', ']'),
        ('^', '**')
    ]
    for old, new in li:
        expression = expression.replace(old, new)
    return expression.lower()

def to_sympy(e):
    return add_multiplication(convert(e))


def separate(expr, classes_dict):
    di = {}
    not_const_terms = []
    for key, term in classes_dict.items():
        if key == CONSTANT_TERM_KEY:
            continue
        not_const_terms.append(term)
        di[key] = expr.coeff(term)

    constant_term, _ = expr.as_independent(*not_const_terms)
    return {**di, CONSTANT_TERM_KEY: constant_term}


def flatten(li):
    for sublist in li:
        yield from sublist


def __eval_avoid_namespace_pollution(string):
    return eval(string)

def main(in_file, out_file, dim, classes_dict_callback):
    data = {}

    with open(in_file, 'r') as fp:
        input_str = fp.read()

    python_list = eval(to_sympy(input_str))

    print(python_list)

    for _ in range(dim - 1):
        python_list = sum(python_list, [])

    print(python_list)

    for key, expr in python_list:
        if isinstance(key, list):
            key = tuple(key)
        data[key] = separate(expr, classes_dict_callback(*key))

    from pprint import pprint
    pprint(data)

    with open(out_file, 'w') as fp:
        fp.write('from sympy import *\n')
        fp.write('from sympy.abc import *\n')
        fp.write('_data = \\\n')
        pprint(data, stream=fp)
        fp.write('\n')





