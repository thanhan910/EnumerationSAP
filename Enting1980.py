from utils import x_pow

"""
Enumerate self-avoiding polygons on a 3xn square lattice.
"""

def n3_A1(n):
    if n <= 1:
        return x_pow(2)
    return x_pow(2) * n3_A1(n - 1) + 2 * x_pow(3) * n3_A2(n - 1)


def n3_A2(n):
    if n <= 1:
        return x_pow(1)
    return x_pow(3) * n3_A1(n - 1) + x_pow(2) * n3_A2(n - 1)

def n3_G(n):
    return x_pow(4) * n3_A1(n - 1) + 2 * x_pow(3) * n3_A2(n - 1)


def G(m, n):
    if m == 3:
        return n3_G(n)
    return x_pow(1)

def g(m, n):
    return G(m, n) + G(m - 1, n) * -2 + G(m - 2, n)
