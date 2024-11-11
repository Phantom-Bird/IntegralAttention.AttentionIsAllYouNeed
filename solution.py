from typing import Iterable, Callable, TypeVar
from sympy import *


class CannotCalculate(Exception):
    pass


class Solution:
    MAX_CALCULATE = 4
    MAX_TRY = 4
    CONSTANT_TERM_KEY = 'constant_term'

    Arg = TypeVar('Arg')
    TryDetails = TypeVar('TryDetails')

    solve_args_keys: tuple[str, ...]
    tries: Callable[[], Iterable]
    symbols: tuple[Symbol, ...]

    check_valid: Callable[[Arg, ...], str | None]

    integrate_formula: Callable[[TryDetails], Expr]
    integrate_args: tuple[Symbol, int | float, int | float]

    integrate_result_classes: dict[str, Expr | None]
    integrate_result_classes_minus: Callable[[Arg, ...], dict[str, Expr]]

    check_sgn: Callable[[int | float, ...], 1 | 0 | -1]

    get_latex_output: Callable[[str, int | float, ..., 1 | 0 | -1], str]
    cannot_solve: str

    def integrate_and_separate(self, n: int, solve_args) -> dict[str, Expr]:
        """解积分，分离各项"""
        if n > self.MAX_CALCULATE:
            raise CannotCalculate()

        # 解积分
        res = integrate(self.integrate_formula(n), self.integrate_args)
        res = expand(expand(res))
        print(f'integrate[0,1] {self.integrate_formula(n)}={res}')

        # 分离各项
        di = {}
        exprs = []
        for key, expr in self.integrate_result_classes.items():
            if key == self.CONSTANT_TERM_KEY:
                continue
            exprs.append(expr)
            di[key] = res.coeff(expr)

        constant_term, _ = res.as_independent(*exprs)
        return {**di, self.CONSTANT_TERM_KEY: constant_term}

    def get_symbols(self, n: int, solve_args, separate_result):
        """凑积分结果系数"""
        system = [
            int_term - self.integrate_result_classes_minus(*solve_args)[key]
            for key, int_term in separate_result.items()
        ]
        return linsolve(system, *self.symbols)

    def try_times(self, solve_args) -> tuple[int, tuple, int] | None:
        for i in self.tries():
            separate = self.integrate_and_separate(i, solve_args)
            for symbol_solution in self.get_symbols(i, solve_args, separate):
                if sgn := self.check_sgn(*symbol_solution):
                    return i, symbol_solution, sgn
        return None

    def get_latex_ans(self, *solve_args):
        if (invalid := self.check_invalid(*solve_args)) is not None:
            return invalid
        try:
            res = self.try_times(solve_args)
        except CannotCalculate:
            res = None

        if res is None:
            return self.cannot_solve

        n, symbol_solution, sgn = res
        print(f'{(n, symbol_solution, sgn)=}')
        i = self.integrate_formula(n).subs(list(zip(self.symbols, symbol_solution)))

        int_sym, int_low, int_high = self.integrate_args
        return self.get_latex_output(rf'\int_{int_low}^{int_high} {latex(i)} \mathrm{{d}} {int_sym}', *solve_args, sgn)

