"""
PiNIF[n_, m_] :=
 Collect[PowerExpand[
   Expand[ Integrate[
     x^m*(a + b x^2)*(Log[1/x])^(n - 1)/(x^2 + 1), {x, 0, 1}]]], Pi^n]
"""
