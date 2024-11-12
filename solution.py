from typing import Iterable, Callable
from sympy import *


solutions = {}
top_solution_name = None

def register(name, solution, top=False):
    global top_solution_name
    solutions[name] = solution
    if top or top_solution_name is None:
        top_solution_name = name


class CannotCalculate(Exception):
    pass


class BadInput(Exception):
    pass


CONSTANT_TERM_KEY = 'constant_term'


class GetIntegrate:
    integrate_result_classes: dict[str, Expr | None]

    def integrate_and_separate(self, integrate_formula: Expr, integrate_args: tuple) -> dict[str, Expr]:
        """解积分，分离各项"""
        raise NotImplementedError('该函数已弃用，请使用 GetIntegrateFromData 类。如果想要使用它预处理，见 pre/old_solution.py')
        # # 解积分
        # res = integrate(integrate_formula, integrate_args)
        # res = expand(expand(res))
        # print(f'integrate[0,1] {integrate_formula}={res}')
        #
        # # 分离各项
        # di = {}
        # exprs = []
        # for key, expr in self.integrate_result_classes.items():
        #     if key == CONSTANT_TERM_KEY:
        #         continue
        #     exprs.append(expr)
        #     di[key] = res.coeff(expr)
        #
        # constant_term, _ = res.as_independent(*exprs)
        # return {**di, CONSTANT_TERM_KEY: constant_term}

    def get_integrate_args(self, try_arg):
        raise NotImplementedError()

    def tries(self, try_arg):
        return self.integrate_and_separate(*self.get_integrate_args(try_arg))

    def get_latex(self, try_arg, subs):
        expr, args = self.get_integrate_args(try_arg)
        expr = simplify(expr).subs(subs)
        sym, low, high = args
        return r'\int_{%s}^{%s} {%s} \mathrm{d} {%s}' % (low, high, latex(expr), sym)


class GetIntegrateFromData(GetIntegrate):
    data: dict[object, dict[str, Expr]]

    def tries(self, try_arg):
        return self.data[try_arg]


class Solution:
    MAX_CALCULATE = 4
    MAX_TRY = 4

    get_integrate: GetIntegrate

    get_tries_args: Callable[[], Iterable[Expr]]
    symbols: tuple[Symbol, ...]

    integrate_result_classes_eq: dict[str, Expr]

    check_sgn: Callable
    # check_sgn: Callable[?, 1 | 0 | -1]

    def __init__(self, *args):
        raise NotImplementedError()

    def get_symbols(self, separate_result):
        """凑积分结果系数"""
        system = [
            Eq(int_term, self.integrate_result_classes_eq[key])
            for key, int_term in separate_result.items()
        ]
        print(f'{system=}')
        return linsolve(system, *self.symbols)

    def try_times(self) -> tuple[Expr, dict, int] | tuple[None, None, None]:
        for try_arg in self.get_tries_args():
            separate = self.get_integrate.tries(try_arg)
            for symbol_solution in self.get_symbols(separate):
                if sgn := self.check_sgn(*symbol_solution):
                    return try_arg, dict(zip(self.symbols, symbol_solution)), sgn
        return None, None, None

    def get_latex_ans(self):
        raise NotImplementedError()
