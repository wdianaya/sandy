import math

def poln_kvadr_uravn(a, b, c):
    discr = (b ** 2) - (4 * a * c)

    x1 = 0
    x2 = 0

    if discr > 0:
        x1 = -b + math.sqrt(discr) / (2 * a)
        x2 = (-b - math.sqrt(discr) / (2 * a))
    elif discr == 0:
        x1 = -b + math.sqrt(discr) / (2 * a)
        x2 = x1
    elif discr < 0:
        x1 = 'нет корней'
        x2 = x1

    return x1, x2



