# PiNI[n_, m_] := Integrate[x^m*(a + b x^2)*(Log[1/x])^(n - 1)/(x^2 + 1), {x, 0, 1}]
# PiNIF[n_, m_] := Collect[PowerExpand[Expand[PiNI[n, m]]], Pi^n]
# results =
#  Table[Table[ { n, 2*m + 1 - Mod[n, 2],
#                 PiNIF[n, 2*m + 1 - Mod[n, 2]]},
#              {m, 6}], {n, 6}]

from pre.mma2sympy import *

if __name__ == '__main__':
    in_file = '../mma2sympy_input.txt'
    out_file = '../mma2sympy_output.py'

    def get_classes_dict(n, m):
        return {
            'pin_term': pi ** n,
            CONSTANT_TERM_KEY: None
        }

    main(in_file, out_file, 2, get_classes_dict)
