import math
from sympy import symbols, Eq, solve, sympify

def system_double(urs):
    eq_urs = []
    x, y = symbols('x y')
    for elem in urs:
        eq_urs.append(Eq(sympify(elem.split('=')[0]), sympify(elem.split('=')[1])))
    return solve(eq_urs, (x, y))

def system_triple(urs):
    eq_urs = []
    x, y, z = symbols('x y z')
    for elem in urs:
        eq_urs.append(Eq(sympify(elem.split('=')[0]), sympify(elem.split('=')[1])))
    return solve(eq_urs, (x, y, z))

def uravn(ur):
    x = symbols('x')
    uravn = Eq(sympify(ur.split('=')[0]), sympify(ur.split('=')[1]))
    return solve(uravn, (x))

print(uravn('x**4 + x ** 3 + x**2 + x=30'))

