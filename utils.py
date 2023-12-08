import numpy as np

def x_pow(n):
    return np.polynomial.Polynomial([0] * n + [1])

def repr_polynomial(v):
    """
    Convert a polynomial representation from a vector to string.
    """
    s = []
    for i in range(len(v)):
        if v[i] != 0:
            p = f"x^{i}"
            if v[i] != 1:
                if v[i] % 1 == 0:
                    p = f"{int(v[i])}{p}"
                else:
                    p = f"{v[i]}*{p}"
            s.append(p)
    return " + ".join(s)

def multiply_two_polynomials(a, b):
    """
    Multiply two polynomials represented as vectors.
    """
    c = np.zeros(len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            c[i + j] += a[i] * b[j]
    return c

def sum_polynomials(*polynomials):
    """
    Sum multiple polynomials represented as vectors.
    """
    max_len = max([len(p) for p in polynomials])
    s = np.zeros(max_len)
    for p in polynomials:
        for i in range(len(p)):
            s[i] += p[i]
    return s
