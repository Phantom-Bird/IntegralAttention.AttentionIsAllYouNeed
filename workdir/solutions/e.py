from solution import *
from sympy import *
from sympy.abc import a, b, x
from sgntools import lin_func_sgn
from gui import guilib as g
from output_util import to_latex, sign2cmp


class EIntegrate(GetIntegrateFromData):
    # sympy 算力不够，以下由 MMA 算出
    data = {
        1: {
            'e_term': -a + 3*b,
            CONSTANT_TERM_KEY: 3*a - 8*b,
        },
        2: {
            'e_term': 2 * (7*a - 32*b),
            CONSTANT_TERM_KEY: 2 * (-19*a + 87*b),
        },
        3: {
            'e_term': 6 * (71*a + 465*b),
            CONSTANT_TERM_KEY: 6 * (193*a - 1264*b),
        },
    }

    def get_integrate_args(self, n):
        return x ** n * (1 - x) ** n * (a + b * x) * exp(x), (x, 0, 1)


class ESolution(Solution):
    gui = [
        '比较 e 与',
        g.Frac(g.Entry(vid='p'),
               g.Entry(vid='q'))
    ]

    def __init__(self, p, q):
        self.p = p
        self.q = q

        if self.q == 0:
            raise BadInput()

        self.get_integrate = EIntegrate()
        self.symbols = (a, b)

        self.integrate_result_classes_eq = {
            'e_term': q,
            CONSTANT_TERM_KEY: -p,
        }
        # check
        self.check_sgn = lin_func_sgn

    @staticmethod
    def get_tries_args():
        return range(1, 4)

    def get_latex_ans(self):
        try_arg, symbol_val, sgn = self.try_times()
        print(f'{(try_arg, symbol_val, sgn)=}')

        if try_arg is None:
            return None

        p = to_latex(self.p)
        q = to_latex(self.q, is_coeff=True)
        I = self.get_integrate.get_latex(try_arg, symbol_val)
        return rf'{q}e-{p} = {I} {sign2cmp[sgn]} 0'


register('e', ESolution)


if __name__ == '__main__':
    print(ESolution(25, 9))
