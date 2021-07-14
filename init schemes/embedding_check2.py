import matplotlib.pyplot as plt
import numpy as np
import copy


def compare(pi, pi0):
    return np.prod(pi == pi0)


def extract(pi, S):
    result = []

    for item in pi:
        if item in S:
            result.append(item)

    assert (len(result) == len(S))
    return np.array(result)


def calculate_DG(pi, pi0):
    n = len(pi)
    assert (len(pi0) == n)
    result = 0

    for k in range(n):
        for j in range(k):
            for i in range(j):
                tmp = extract(pi, [i, j, k])
                tmp0 = extract(pi0, [i, j, k])

                if compare(tmp, tmp0) or compare(tmp[[1, 2, 0]], tmp0) or compare(tmp[[2, 0, 1]], tmp0):
                    continue
                else:
                    result += 1
    return result


def calculate_K(pi, pi0):
    n = len(pi)
    assert (len(pi0) == n)
    result = 0

    for j in range(n):
        for i in range(j):
            tmp = extract(pi, [i, j])
            tmp0 = extract(pi0, [i, j])

            if compare(tmp, tmp0[[1, 0]]):
                result += 1
    return result


def rank_vector(pi):
    pi = list(pi)
    n = len(pi)
    result = []

    for i in range(n):
        result.append(pi.index(i))

    return np.array(result)


def calculate_S_sq(pi, pi0):
    r = rank_vector(pi)
    r0 = rank_vector(pi0)

    return np.linalg.norm(r - r0) ** 2


def calculate_S_sq2(pi, pi0):
    return np.linalg.norm(pi - pi0) ** 2


repeats = 1000
n = 20

Spearman_rho_sq = np.zeros(repeats)
Spearman_rho_sq2 = np.zeros(repeats)
Kendall_tau = np.zeros(repeats)
Daniels_Guilbaud = np.zeros(repeats)
sanity_check = np.zeros(repeats)

for i in range(repeats):
    pi = np.random.permutation(n)
    pi_ = np.random.permutation(n)

    Spearman_rho_sq[i] = calculate_S_sq(pi, pi_)
    Spearman_rho_sq2[i] = calculate_S_sq2(pi, pi_)
    Kendall_tau[i] = calculate_K(pi, pi_)
    Daniels_Guilbaud[i] = calculate_DG(pi, pi_)
    sanity_check[i] = n * Kendall_tau[i] - Daniels_Guilbaud[i]


plt.figure(1)
plt.scatter(Spearman_rho_sq, sanity_check)

plt.figure(2)
plt.scatter(Spearman_rho_sq, Kendall_tau)

plt.figure(3)
plt.scatter(Spearman_rho_sq2, Kendall_tau)

plt.figure(4)
plt.scatter(Spearman_rho_sq, Daniels_Guilbaud)

plt.show()
# plt.savefig("sanity.png", dpi=600)
