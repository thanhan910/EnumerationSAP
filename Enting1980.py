from utils import sum_polynomials

import numpy as np

"""
Enumerate self-avoiding polygons on a 3xn square lattice.
"""

def n3_A1(n):
    if n <= 1:
        return np.array([0, 0, 1])
    ans = sum_polynomials(
        np.append([0, 0], n3_A1(n - 1)),
        np.append([0, 0, 0], n3_A2(n - 1) * 2)
    )
    return ans


def n3_A2(n):
    if n <= 1:
        return np.array([0, 1])
    return sum_polynomials(
        np.append([0, 0, 0], n3_A1(n - 1)),
        np.append([0, 0], n3_A2(n - 1))
    )

def n3_G(n):
    return sum_polynomials(
        np.append([0, 0, 0, 0], n3_A1(n - 1)),
        np.append([0, 0, 0], n3_A2(n - 1) * 2)
    )


def G(m, n):
    if m == 3:
        return n3_G(n)
    return np.array([0]) # temporary stub

def g(m, n):
    return sum_polynomials(
        G(m, n),
        G(m - 1, n) * -2,
        G(m - 2, n)
    )
