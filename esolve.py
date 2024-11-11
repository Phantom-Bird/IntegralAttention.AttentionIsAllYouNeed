from solution import Solution
from sympy import *
from sympy.abc import a, b, x
from fxtools import lin_func_sgn

class ESolution(Solution):
    def __init__(self):
        # args
        self.solve_arg_keys = ('p', 'q'),
        self.tries = lambda: range(1, 4)
        self.symbols = (a, b)
        # pre
        self.check_invalid = lambda p, q: '你莫不是在消遣洒家？' if q == 0 else None
        # integrate
        self.integrate_formula = lambda n: x ** n * (1 - x) ** n * (a + b * x) * exp(x)
        self.integrate_args = (x, 0, 1)
        # classes
        self.integrate_result_classes = {
            'e_term': exp(1),
            self.CONSTANT_TERM_KEY: None,
        }
        self.integrate_result_classes_minus = lambda p, q: {
            'e_term': q,
            self.CONSTANT_TERM_KEY: -p,
        }
        # check
        self.check_sgn = lin_func_sgn

        # output
        def get_latex_output(I, p, q, sgn):
            return rf'注意到 $${q if q != 1 else ""}e-{p} = {I} {">" if sgn == 1 else "<"} 0$$ 证毕！'

        self.get_latex_output = get_latex_output
        self.cannot_solve = '注意力涣散……'


if __name__ == '__main__':
    print(ESolution().get_latex_ans(25, 9))
