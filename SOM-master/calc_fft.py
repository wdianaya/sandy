from numpy import arange
from scipy.fft import fft

def calc_fft(a):
    fs = 10
    n = len(a)
    k = arange(n)
    T = n / fs
    frq = k / T
    frq = frq[range(int(n / 2))]

    y = fft(a) / n
    y = y[range(int(n / 2))]
    return y

