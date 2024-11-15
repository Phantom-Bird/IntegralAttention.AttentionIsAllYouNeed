from pre.mma2sympy import *
from sympy.abc import q


if __name__ == '__main__':
    in_file = 'mma2sympy_input.txt'
    out_file = 'mma2sympy_output.py'

    def get_classes_dict(n):
        return {
            'eq_term': e ** q,
            CONSTANT_TERM_KEY: None
        }

    main(in_file, out_file, 1, get_classes_dict)
