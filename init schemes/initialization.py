"""
Created on 2021/03/29
@author: nicklee

(Description)
"""
import numpy as np
import functools
import multiprocessing
import itertools as it
import matplotlib.pyplot as plt
import warnings
import sys


def init_1(n, num_perm):
    """
    Uniform random sampling of permutations, without repetition

    :param n: number of test cases
    :param num_perm: desired number of permutations
    :return: list of
    """
    result = set()
    for i in range(num_perm):
        while True:
            perm = np.random.permutation(n) + 1
            key = tuple(perm)
            if key not in result:
                result.add(key)
                break
    return list(result)


# Includes permutation of every swap distance!
## number of perms at each dist
def num_perms_at_dist(n):
    sk = np.zeros((n + 1, int(n * (n - 1) / 2 + 1)))
    for i in range(n + 1):
        sk[i, 0] = 1
    for i in range(1, 1 + n):
        for j in range(1, int(i * (i - 1) / 2 + 1)):
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    if j - i >= 0:
                        sk[i, j] = sk[i, j - 1] + sk[i - 1, j] - sk[i - 1, j - i]
                    else:
                        sk[i, j] = sk[i, j - 1] + sk[i - 1, j]
                except Warning as e:
                    sk[i, j] = 1e10
    return sk.astype(np.uint64)
    # return sk


def v2ranking(v, n):  ##len(v)==n, last item must be 0
    # n = len(v)
    rem = list(range(n))
    rank = np.array([np.nan] * n)  # np.zeros(n,dtype=np.int)
    # print(v,rem,rank)
    for i in range(len(v)):
        rank[i] = rem[v[i]]
        rem.pop(v[i])
    return rank.astype(int)  # [i+1 for i in permut];


## random permutations at distance
def random_perm_at_dist(n, dist, sk):
    # param sk is the results of the function num_perms_at_dist(n)
    i = 0
    probs = np.zeros(n + 1)
    v = np.zeros(n, dtype=int)
    while i < n and dist > 0:
        rest_max_dist = (n - i - 1) * (n - i - 2) / 2
        if rest_max_dist >= dist:
            probs[0] = sk[n - i - 1, dist]
        else:
            probs[0] = 0
        mi = min(dist + 1, n - i)
        for j in range(1, mi):
            if rest_max_dist + j >= dist:
                probs[j] = sk[n - i - 1, dist - j]
            else:
                probs[j] = 0
        v[i] = np.random.choice(mi, 1, p=probs[:mi] / probs[:mi].sum())
        dist -= v[i]
        i += 1
    return v2ranking(v, n)


def perms_at_dist(n, sk, dist):
    """
    Uniform random sampling of permutations with 'dist' inversions

    :param dist: prescribed Kendall tau distance
    :return: list of
    """
    num_perm = int(min(10, sk[n, dist]))

    result = set()
    for i in range(num_perm):
        while True:
            perm = random_perm_at_dist(n, dist, sk) + 1
            key = tuple(perm)
            if key not in result:
                result.add(key)
                break
    return list(result)


def init_2(n):
    sk = num_perms_at_dist(n)

    with multiprocessing.Pool() as pool:
        all_permutations = pool.map(functools.partial(perms_at_dist, n, sk), range(int(1 + n*(n-1)/2)))
    # print(all_permutations[-1])
    return [perm for sublist in all_permutations for perm in sublist]


def kendallTau(A, B=None):
    # if any partial is B
    if B is None:
        B = list(range(1, 1+len(A)))
    n = len(A)
    pairs = it.combinations(range(n), 2)
    distance = 0
    for x, y in pairs:
        # if not A[x]!=A[x] and not A[y]!=A[y]:#OJO no se check B
        a = A[x] - A[y]
        try:
            b = B[x] - B[y]  # if discordant (different signs)
        except:
            print("ERROR kendallTau, check b", A, B, x, y)
        # print(b,a,b,A, B, x, y,a * b < 0)
        if a * b < 0:
            distance += 1
    return distance


if __name__ == "__main__":
    # a = init_2(20)
    # print(a[-1])

    n = 200

    # with multiprocessing.Pool() as pool:
    #     kendall_distances_2 = pool.map(kendallTau, init_2(n))
    # plt.hist(kendall_distances_2, bins=100)
    # plt.show()
    # print(kendall_distances_2)

    perms = init_1(n, 2**15)
    pivot = perms[10]

    def auxiliary(perm):
        return kendallTau(pivot, perm)

    with multiprocessing.Pool() as pool:
        # kendall_distances_1 = pool.map(kendallTau, init_1(n, 10000))
        kendall_distances_1 = pool.map(auxiliary, perms)
    plt.hist(kendall_distances_1, bins=100)
    plt.show()
