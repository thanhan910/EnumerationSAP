from utils import x_pow

import numpy as np

"""
Enumerate self-avoiding polygons on a 3xn square lattice.
"""

def element_exists(dict2d, m ,n):
    if m < 0 or n < 0:
        return False
    if m not in dict2d:
        return False
    if n not in dict2d[m]:
        return False
    return dict2d[m][n] != -1

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

# A 2D array of size 50x50 to store results of subproblems
CONST_BIG_G = {}
CONST_SMALL_G = {}

def G_big(m, n):
    '''
    Polynomial representations of self-avoiding polygons that fit within a m x n rectangle and span the entire length n.
    sum of u(i) * x^i
    u(i) = number of self-avoiding polygons of length i that fit within a m x n rectangle and span the entire length n.
    '''
    if m not in CONST_BIG_G:
        CONST_BIG_G[m] = {}
    if m <= 1 or n <= 1:
        return np.polynomial.Polynomial([0])
    if element_exists(CONST_BIG_G, m, n):
        return CONST_BIG_G[m][n]
    if m == 2:
        CONST_BIG_G[m][n] = x_pow(n * 2)
        return CONST_BIG_G[m][n]
    if m == 3:
        CONST_BIG_G[m][n] = n3_G(n)
        return CONST_BIG_G[m][n]
    return x_pow(1) # TODO: implement this

def g_small(m, n):
    '''
    Polynomial representations of self-avoiding polygons that fit within a m x n rectangle and span the entire length n and width m.
    sum of u(i) * x^i
    u(i) = number of self-avoiding polygons of length i that fit within a m x n rectangle and span the entire  length n and width m.
    '''
    if element_exists(CONST_SMALL_G, m, n):
        return CONST_SMALL_G[m][n]
    if m not in CONST_SMALL_G:
        CONST_SMALL_G[m] = {}
    CONST_SMALL_G[m][n] = G_big(m, n) + G_big(m - 1, n) * -2 + G_big(m - 2, n)
    return CONST_SMALL_G[m][n]

def enumerate_saps(size):
    if size <= 3 or size % 2 == 1:
        return 0
    size_half = size // 2
    P = np.polynomial.Polynomial([0])
    for w in range(2, (size_half // 2) + 2):
        P += g_small(w, w)
    for l in range(2, size_half + 1):
        for w in range(2, l):
            if (l + w) > size_half + 2:
                break
            P += g_small(w, l) * 2
    return P.coef[size]