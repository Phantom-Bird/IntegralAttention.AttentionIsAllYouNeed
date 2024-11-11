from jsoncache import DictJsonConverter, cache_to_json
from fxtools import sq_func_sgn

from collections import namedtuple
from sympy import *
from sympy.abc import a, b, c, x

class CannotCalculate(Exception): pass


MAX_CALCULATE = 4
MAX_TRY = 4
CONSTANT_TERM_KEY = 'constant_term'

args = 2,  # p, q
tries = True,  # give arg n to lambda
symbols = (a, b, c)
integrate_formula = lambda n: x ** n * (1 - x) ** n * (a + b * x + c * x ** 2) / (1 + x ** 2)
integrate_args = (x, 0, 1)
integrate_result_classes = {
    'pi_term': pi,
    'log2_term': log(2),
    CONSTANT_TERM_KEY: None,
}
integrate_result_classes_minus = lambda p, q: {
    'pi_term': q,
    'log2_term': 0,
    CONSTANT_TERM_KEY: -p,
}
integrate_constant = lambda p, q: -p
check_sgn = sq_func_sgn

converter = DictJsonConverter(str, sympify)

# @cache_to_json('pi_integrate_cache.json', converter)
def get_pi_integrate(n: int, p: int, q: int) -> dict:
    """解积分，分离各项"""
    if n > MAX_CALCULATE:
        raise CannotCalculate()

    # 解积分
    res = integrate(integrate_formula(n), integrate_args)
    res = expand(expand(res))

    # 分离各项
    di = {}
    exprs = []
    for key, expr in integrate_result_classes.items():
        if key == CONSTANT_TERM_KEY:
            continue
        exprs.append(expr)
        di[key] = res.coeff(expr)

    constant_term, _ = res.as_independent(*exprs)
    return {**di, CONSTANT_TERM_KEY: constant_term}


def get_one_abc(n: int, p: int, q: int):
    """凑积分结果系数"""
    system = [
        int_term - integrate_result_classes_minus(p, q)[key]
        for key, int_term in get_pi_integrate(n, p, q).items()
    ]
    return linsolve(system, *symbols)


def solve_pi(p: int, q: int) -> tuple[int, tuple, int] | None:
    """pi =?= p/q"""
    for i in range(1, MAX_TRY+1):
        for symbol_solution in get_one_abc(i, p, q):
            if sgn := check_sgn(*symbol_solution):
                return i, symbol_solution, sgn
    return None


def pi_get_latex_ans(p: int, q: int):
    if q == 0:
        return '你莫不是在消遣洒家？'
    try:
        res = solve_pi(p, q)
    except CannotCalculate:
        res = None

    if res is None:
        return r'注意力不集中……'

    n, symbol_solution, sgn = res
    print(f'{(n, symbol_solution, sgn)=}')
    i = integrate_formula(n).subs(list(zip(symbols, symbol_solution)))
    return rf'注意到 $${q if q!=1 else ""}\pi-{p} = \int_0^1 {latex(i)} \mathrm{"{d}"} x {">" if sgn==1 else "<"} 0$$ 证毕！'


# for i in range(1, 6):
#     print(f'{i=}, {get_pi_integrate(i)=}')

# print(pi_get_latex_ans(25, 8))
