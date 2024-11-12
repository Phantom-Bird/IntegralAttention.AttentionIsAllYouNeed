from sympy import *


CONSTANT_TERM_KEY = 'constant_term'


class GetIntegrate:
    integrate_result_classes: dict[str, Expr | None]

    def integrate_and_separate(self, integrate_formula: Expr, integrate_args: tuple) -> dict[str, Expr]:
        """解积分，分离各项"""
        # 解积分
        res = integrate(integrate_formula, integrate_args)
        res = expand(expand(res))
        print(f'integrate[0,1] {integrate_formula}={res}')

        # 分离各项
        di = {}
        exprs = []
        for key, expr in self.integrate_result_classes.items():
            if key == CONSTANT_TERM_KEY:
                continue
            exprs.append(expr)
            di[key] = res.coeff(expr)

        constant_term, _ = res.as_independent(*exprs)
        return {**di, CONSTANT_TERM_KEY: constant_term}

    def get_integrate_args(self, try_arg):
        raise NotImplementedError()

    def tries(self, try_arg):
        return self.integrate_and_separate(*self.get_integrate_args(try_arg))

    def get_latex(self, try_arg, subs):
        expr, args = self.get_integrate_args(try_arg)
        expr = simplify(expr).subs(subs)
        sym, low, high = args
        return r'\int_{%s}^{%s} {%s} \mathrm{d} {%s}' % (low, high, latex(expr), sym)
