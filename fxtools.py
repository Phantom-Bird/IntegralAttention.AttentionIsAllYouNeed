def sq_func_sgn(a, b, c):
    r"""
    let f(x) = a+bx+cx^2, x \in [0, 1]
    :return: f(x)>=0? 1; f(x)<=0? -1; 0
    """
    f0 = a
    f1 = a + b + c
    fm = 0

    if c != 0:
        x_m = -b / (2 * c)
        if 0 <= x_m <= 1:
            fm = a + b * x_m + c * x_m ** 2

    if f0 >= 0 and f1 >= 0 and fm >= 0:
        return 1
    if f0 <= 0 and f1 <= 0 and fm <= 0:
        return -1
    return 0
