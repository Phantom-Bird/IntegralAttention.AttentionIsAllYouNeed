from sympy import *
from sympy.abc import *

_data = \
    {1: {'constant_term': 3 * a - 8 * b, 'e_term': -a + 3 * b},
     2: {'constant_term': -38 * a + 174 * b, 'e_term': 14 * a - 64 * b},
     3: {'constant_term': 1158 * a - 7584 * b, 'e_term': -426 * a + 2790 * b},
     4: {'constant_term': -65304 * a + 557400 * b, 'e_term': 24024 * a - 205056 * b},
     5: {'constant_term': 5900520 * a - 62118720 * b,
         'e_term': -2170680 * a + 22852200 * b},
     6: {'constant_term': -780827760 * a + 9778048560 * b,
         'e_term': 287250480 * a - 3597143040 * b}}
