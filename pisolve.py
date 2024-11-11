from solution import *
from sympy import *
from sympy.abc import a, b, c, x
from fxtools import sq_func_sgn

class PiSolution(Solution):
    def __init__(self):
        # args
        self.solve_arg_keys = ('p', 'q'),
        self.tries = lambda: range(1, 5)
        self.symbols = (a, b, c)
        # pre
        self.check_invalid = lambda p, q: '你莫不是在消遣洒家？' if q == 0 else None
        # integrate
        self.integrate_formula = lambda n: x ** n * (1 - x) ** n * (a + b * x + c * x ** 2) / (1 + x ** 2)
        self.integrate_args = (x, 0, 1)
        # classes
        self.integrate_result_classes = {
            'pi_term': pi,
            'log2_term': log(2),
            self.CONSTANT_TERM_KEY: None,
        }
        self.integrate_result_classes_minus = lambda p, q: {
            'pi_term': q,
            'log2_term': 0,
            self.CONSTANT_TERM_KEY: -p,
        }
        # check
        self.check_sgn = sq_func_sgn

        # output
        def get_latex_output(I, p, q, sgn):
            return rf'注意到 $${q if q != 1 else ""}\pi-{p} = {I} {">" if sgn == 1 else "<"} 0$$ 证毕！'

        self.get_latex_output = get_latex_output
        self.cannot_solve = '注意力涣散……'
