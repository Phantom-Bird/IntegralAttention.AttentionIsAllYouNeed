from jsoncache import NamedTupleJsonConverter, cache_to_json
from fxtools import sq_func_sgn

from collections import namedtuple
from sympy import *
from sympy.abc import a, b, c, x

class CannotCalculate(Exception): pass


MAX_CALCULATE = 4
MAX_TRY = 4
def I(n: int) -> Expr:
    return x ** n * (1 - x) ** n * (a + b * x + c * x ** 2) / (1 + x ** 2)


EIntegrateResult = namedtuple(
    'EIntegrateResult',
    {
        'e_term': Expr,
        'constant_term': Expr,
    }
)

converter = NamedTupleJsonConverter(PiIntegrateResult, str, sympify)

@cache_to_json('pi_integrate_cache.json', converter)
def get_pi_integrate(n: int) -> PiIntegrateResult:
    """解积分，分离各项"""
    if n > MAX_CALCULATE:
        raise CannotCalculate()

    res = integrate(I(n), (x, 0, 1))
    res = expand(expand(res))

    pi_term = res.coeff(pi)
    log2_term = res.coeff(log(2))
    constant_term, _ = res.as_independent(pi, log(2))

    return PiIntegrateResult(pi_term, log2_term, constant_term)


def get_one_abc(n: int, p: int, q: int):
    """凑积分结果系数"""
    pi_term, log2_term, constant_term = get_pi_integrate(n)
    return linsolve((pi_term - q, log2_term, constant_term + p), a, b, c)


def solve_e(p: int, q: int) -> tuple[int, int, int, int, int] | None:
    """pi =?= p/q"""
    for i in range(1, MAX_TRY+1):
        for a, b, c in get_one_abc(i, p, q):
            if sgn := sq_func_sgn(a, b, c):
                return i, a, b, c, sgn
    return None


def e_get_latex_ans(p: int, q: int):
    if q == 0:
        return '你莫不是在消遣洒家？'
    try:
        res = solve_e(p, q)
    except CannotCalculate:
        res = None

    if res is None:
        return r'注意力不集中……'

    n, a_, b_, c_, sgn = res
    i = I(n).subs({a: a_, b: b_, c: c_})
    return rf'注意到 $${q if q!=1 else ""}e-{p} = \int_0^1 {latex(i)} \mathrm{"{d}"} x {">" if sgn==1 else "<"} 0$$ 证毕！'


# for i in range(1, 6):
#     print(f'{i=}, {get_pi_integrate(i)=}')

# print(pi_get_latex_ans(25, 8))
