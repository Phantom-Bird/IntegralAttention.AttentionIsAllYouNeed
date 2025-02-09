# Attention is all you need

> 注意：本项目和 AI 中的注意力机制没有一毛钱关系。

灵感及理论来源：[量化调酒师](https://www.zhihu.com/people/plel)

## 下载使用

```shell
python -m pip install -r requirements.txt
python workdir/main.py
```

> $\LaTeX$ 的渲染可能会奇慢无比，此时你可以将 `config.py` 中的 `MATHJAX` 改为更快的 CDN 的地址。
> 当然，渲染最快的方法是把 MathJax 下载到 `workdir` 目录下，然后把 JS 文件的相对路径填到 `MATHJAX` 常量里。

## 插件编写

例：编写比较 $e^q$ 与 $\frac{u}{v}$ 大小的插件

### 公式选择

$$\int_0^1 x^n (1-x)^n (a+bx) e^{qx} \mathrm{d} x=f(a, b, q)e^q+g(a, b, q)$$

### 预处理

预处理是指对于所有的 $n$，预处理出 $f$ 以及 $g$ 的过程。  
我们使用 Mathematica 做计算（由于 sympy 的局限性，有一些积分式不能完全化简）  

```mathematica
(* 定义积分式 *)
EQI[n_, q_] := Integrate[x^n (1 - x)^n (a + b x) E^(q x), {x, 0, 1}]
(* 合并 E^q 项 *)
EQICollect[n_, q_] := Collect[Expand[EQI[n, q]], E^q]
(* 批量预处理。*)
(* 需要用 {args, result} 的形式把参数包括进 Table *)
Table[{{n}, EQICollect[n, q]}, {n, 1, 3}]
```

结果（不需要可读性，程序会自动处理）：

```mathematica
{{{1}, E^q ((6 b)/q^4 - (2 a)/q^3 - (4 b)/q^3 + a/q^2 + b/q^2) - (
   6 b)/q^4 + (2 a)/q^3 - (2 b)/q^3 + a/q^2}, {{2}, 
  E^q (-((120 b)/q^6) + (24 a)/q^5 + (72 b)/q^5 - (12 a)/q^4 - (18 b)/
      q^4 + (2 a)/q^3 + (2 b)/q^3) + (120 b)/q^6 - (24 a)/q^5 + (
   48 b)/q^5 - (12 a)/q^4 + (6 b)/q^4 - (2 a)/q^3}, {{3}, 
  E^q ((5040 b)/q^8 - (720 a)/q^7 - (2880 b)/q^7 + (360 a)/q^6 + (
      720 b)/q^6 - (72 a)/q^5 - (96 b)/q^5 + (6 a)/q^4 + (6 b)/
      q^4) - (5040 b)/q^8 + (720 a)/q^7 - (2160 b)/q^7 + (360 a)/
   q^6 - (360 b)/q^6 + (72 a)/q^5 - (24 b)/q^5 + (6 a)/q^4}}
```

接下来，把结果粘贴进 `pre/mma2sympy_input.txt`，并编写预处理程序：

```py
from pre.mma2sympy import *
from sympy.abc import q

in_file = 'mma2sympy_input.txt'
out_file = 'mma2sympy_output.py'

def get_classes_dict(n):
    """返回一个 {名称: 同类项} 的字典"""
    return {
        'eq_term': e ** q,
        CONSTANT_TERM_KEY: None
    }

main(in_file, out_file, 1, get_classes_dict)
# dim=1 代表该 Table 只有一重循环
```

接下来，你可以在 `pre/mma2sympy_output.py` 看到结果：

```py
from sympy import *
from sympy.abc import *

_data = \
    {(1,): {'constant_term': a / q ** 2 + 2 * a / q ** 3 - 2 * b / q ** 3 - 6 * b / q ** 4,
            'eq_term': a / q ** 2 - 2 * a / q ** 3 + b / q ** 2 - 4 * b / q ** 3 + 6 * b / q ** 4},
     (2,): {
         'constant_term': -2 * a / q ** 3 - 12 * a / q ** 4 - 24 * a / q ** 5 + 6 * b / q ** 4 + 48 * b / q ** 5 + 120 * b / q ** 6,
         'eq_term': 2 * a / q ** 3 - 12 * a / q ** 4 + 24 * a / q ** 5 + 2 * b / q ** 3 - 18 * b / q ** 4 + 72 * b / q ** 5 - 120 * b / q ** 6},
     (3,): {
         'constant_term': 6 * a / q ** 4 + 72 * a / q ** 5 + 360 * a / q ** 6 + 720 * a / q ** 7 - 24 * b / q ** 5 - 360 * b / q ** 6 - 2160 * b / q ** 7 - 5040 * b / q ** 8,
         'eq_term': 6 * a / q ** 4 - 72 * a / q ** 5 + 360 * a / q ** 6 - 720 * a / q ** 7 + 6 * b / q ** 4 - 96 * b / q ** 5 + 720 * b / q ** 6 - 2880 * b / q ** 7 + 5040 * b / q ** 8}}

```

### 插件主体

#### `Integrate` 类

我们需要确定 `try_arg`，这是一次尝试附带的参数。
由于我们的代入数据包含 $q$，我们把 $q$ 也包含在 `try_arg` 中。

因为我们的 `try_arg` 与 `data` 的键不一致，所以我们要通过重载 `tries` 进行转换。

```py
from solution import *

...

class EQIntegrate(GetIntegrateFromData):
    data = _data

    def get_integrate_args(self, try_arg):
        n, q = arg
        return x**n * (1-x)**n * (a+b*x) * e**(q*x), (x, 0, 1)

    def tries(self, try_arg):
        n, q_value = try_arg
        return {key: expr.subs(q, q_value)  # 代表将 q 代入 为 q_value
                for key, expr in self.data[(n,)].items()}
```

#### `Solution` 类

```py
from sgntools import lin_func_sgn


class EQSolution(Solution):
    def __init__(self, q1, q2, u, v):
        if q2 == 0 or v == 0:
            raise BadInput()

        self.q = q1 / q2  # 输入都是 Rational 类型的，可以不损失精度相除
        self.u = u
        self.v = v

        self.get_integrate = EQIntegrate()
        self.symbols = (a, b)  # 要求的待定系数

        self.integrate_result_classes_eq = {
            'eq_term': v,
            CONSTANT_TERM_KEY: -u,
        }  # 每个项系数分别要等于的值
        
        self.check_sgn = lin_func_sgn
        # 输入：解包的待定系数的值列表；
        # 输出：0（无法确定），1或-1（可以确定，1和-1哪个代表大于、哪个代表小于，是可以互换的）
        # sgntools 模块提供了 lin_func_sgn 和 sq_func_sgn 函数，详见 help

    def get_tries_args(self):
        """
        生成每一次尝试的 try_arg
        """
        for (n, ) in EQIntegrate.data.keys():
            yield n, self.q
```

#### LaTeX 输出

```py
from output_util import to_latex, to_latexes, sign2cmp

class EQSolution(Solution):
    ...

    def get_latex_ans(self):
        try_arg, symbol_val, sgn = self.try_times()
        print(f'{(try_arg, symbol_val, sgn)=}')

        if try_arg is None:  # 失败
            return None

        p, n = to_latexes(self.p, self.n)  # to_latex(es) 会自动添加 {} 以防优先级混乱
        q = to_latex(self.q, is_coeff=True)  # is_coeff 为 True 时，1 会被忽略
        I = self.get_integrate.get_latex(try_arg, symbol_val)
        return rf'{q}\pi^{n}-{p} = {I} {sign2cmp[sgn]} 0'
```

输入 `print(EQSolution(Rational(2), 1, 7, 1).get_latex_ans())`，可得
$$e^{2}-{7} = \int_{0}^{1} {4 e^{2 x} x^{2} \left(x - 1\right)^{2}} \mathrm{d} {x} > 0$$
我们可以将 `\int_{0}^{1} {4 e^{2 x} x^{2} \left(x - 1\right)^{2}}` 输入 [Wolfram Alpha](https://wolframalpha.com) 验算答案

#### GUI 与 注册

```py
import gui.guilib as g

...

class EQSolution(Solution):
    gui = [
        '比较 e',
        g.Up(g.Frac(g.Entry(vid='q1'),
                    g.Entry(vid='q2'))),
        '与',
        g.Frac(g.Entry(vid='u'),
               g.Entry(vid='v'))
    ]

    ...

register('e^q', EQSolution)
```

将 Python 文件复制到 solution 目录下，运行即可。
