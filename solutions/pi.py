from solution import *
from sympy import *
from sympy.abc import a, b, c, x
from sgntools import sq_func_sgn
from sympy import Rational as R


class PiIntegrate(GetIntegrateFromData):
    # sympy 算力不够，以下由 MMA 算出
    data = {
        1: {
            'pi_term': (a - b - c) / 4,
            'log2_term': (a + b - c) / 2,
            CONSTANT_TERM_KEY: -a + b/2 + 7*c/6,
        },
        2: {
            'pi_term': -b/2,
            'log2_term': a - c,
            CONSTANT_TERM_KEY: (-2*a/3 + 19*b/12 + 7*c/10),
        },
        3: {
            'pi_term': (-a - b + c) / 2,
            'log2_term': a - b - c,
            CONSTANT_TERM_KEY: 53*a/60 + 34*b/15 - 92*c/105,
        },
        4: {
            'pi_term': -a + c,
            'log2_term': 2*b,
            CONSTANT_TERM_KEY: 22*a/7 + 233*b/168 - 1979*c/630,
        },
        5: {
            'pi_term': -a + b + c,
            'log2_term': 2 * (-a - b + c),
            CONSTANT_TERM_KEY: 11411*a/2520 - 4423*b/2520 - 41837*c/9240,
        },
        6: {
            'pi_term': 2 * b,
            'log2_term': -4 * a + 4 * c,
            CONSTANT_TERM_KEY: (38429*a)/13860 - (174169*b)/27720 - (35683*c)/12870,
        }
    }

    def get_integrate_args(self, n):
        return x ** n * (1 - x) ** n * (a + b * x + c * x ** 2) / (1 + x ** 2), (x, 0, 1)


class PiSolution(Solution):
    def __init__(self, p, q):
        self.p = p
        self.q = q

        if self.q == 0:
            raise BadInput()

        self.get_integrate = PiIntegrate()
        self.symbols = (a, b, c)

        self.integrate_result_classes_eq = {
            'pi_term': q,
            'log2_term': 0,
            CONSTANT_TERM_KEY: -p,
        }
        # check
        self.check_sgn = sq_func_sgn

    @staticmethod
    def get_tries_args():
        return range(1, 7)

    def get_latex_ans(self):
        try_arg, symbol_val, sgn = self.try_times()
        print(f'{(try_arg, symbol_val, sgn)=}')

        if try_arg is None:
            return '注意力涣散……'

        p, q = self.p, self.q
        I = self.get_integrate.get_latex(try_arg, symbol_val)
        return rf'注意到 $${q if q != 1 else ""}\pi-{p} = {I} {">" if sgn == 1 else "<"} 0$$ 证毕！'


register('π', PiSolution, top=True)

if __name__ == '__main__':
    while True:
        p = int(input('>>> '))
        q = int(input('  / '))
        print(PiSolution(p, q).get_latex_ans())
