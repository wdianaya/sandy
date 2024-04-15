import random


# Равномерное распределение
def rand_uniform(N, a=0, b=1):
    A = []
    for i in range(N):
        tmp = random.uniform(a, b)
        A.append(tmp)
    return A


# Треугольное распределение
def rand_triang(N, a=0, b=1, mode=1):
    A = []
    for i in range(N):
        tmp = random.triangular(a, b, mode)
        A.append(tmp)
    return A


# Бета распределение
def rand_beta(N, alpha=5, beta=10):
    A = []
    for i in range(N):
        tmp = random.betavariate(alpha, beta)
        A.append(tmp)
    return A


# Экспоненциальное распределение
def rand_expo(N, lambd=1.5):
    A = []
    for i in range(N):
        tmp = random.expovariate(lambd)
        A.append(tmp)
    return A


# Гамма распределение
def rand_gamma(N, alpha=100, beta=2):
    A = []
    for i in range(N):
        tmp = random.gammavariate(alpha, beta)
        A.append(tmp)
    return A


# Нормальное распределение
def rand_gauss(N, mu=100, sigma=50):
    A = []
    for i in range(N):
        tmp = random.gauss(mu, sigma)
        A.append(tmp)
    return A

#Логнормальное распределение
def rand_lognorm(N, mu = 0.0, sigma = 1.0):
    A = []
    for i in range(N):
        tmp = random.lognormvariate(mu, sigma)
        A.append(tmp)
    return A

#Парето распределение
def rand_pareto(N, alpha = 10.0):
    A = []
    for i in range(N):
        tmp = random.paretovariate(alpha)
        A.append(tmp)
    return A
