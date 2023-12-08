from utils import x_pow

import numpy as np

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
    '''
    Polynomial representations of self-avoiding polygons that fit within a m x n rectangle and span the entire length n.
    sum of u(i) * x^i
    u(i) = number of self-avoiding polygons of length i that fit within a m x n rectangle and span the entire length n.
    '''
    if m <= 1 or n <= 1:
        return np.polynomial.Polynomial([0])
    if m == 2:
        return x_pow(n * 2)
    if m == 3:
        return n3_G(n)
    return x_pow(1)

def g(m, n):
    '''
    Polynomial representations of self-avoiding polygons that fit within a m x n rectangle and span the entire length n and width m.
    sum of u(i) * x^i
    u(i) = number of self-avoiding polygons of length i that fit within a m x n rectangle and span the entire  length n and width m.
    '''
    return G(m, n) + G(m - 1, n) * -2 + G(m - 2, n)
