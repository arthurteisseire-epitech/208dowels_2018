import math
from print import print_all

N = 100.0


def main(args):
    x_array = [i for i in range(0, 9)]
    prob = sum(map(lambda x: x[0] * x[1], zip(args, x_array))) / N / 100.0
    tx = list(map(lambda x: lb(N, x, prob) * 100, x_array[:-1]))
    tx.append(100 - sum(tx))

    print_all(args, tx, prob)


def lb(n, k, p):
    prob_ok = pow(p, k)
    prob_ko = pow(1 - p, n - k)
    comb = math.factorial(n) / (math.factorial(k) * math.factorial(n - k))
    return prob_ok * prob_ko * comb
