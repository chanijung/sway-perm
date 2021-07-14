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


n = 20


pi0 = np.random.permutation(n)  # Randomly initialized permutation
pif = (n - 1) - pi0  # Final permutation


mp = {}
for i in range(n):
    mp[pi0[i]] = i

arr = copy.deepcopy(pi0)
for i in range(n):
    arr[i] = mp[pif[i]]

arrPos = [[0 for _ in range(2)] for _ in range(n)]
for i in range(n):
    arrPos[i][0] = arr[i]
    arrPos[i][1] = i
arrPos.sort()

arr0 = np.array(arrPos)[:, 1]
swaps = []

loop = True
while loop:
    loop = False
    for i in range(n - 1):
        if arr0[i] > arr0[i + 1]:
            loop = True
            swaps.append([i, i + 1])
            arr0[[i, i + 1]] = arr0[[i + 1, i]]


l = len(swaps)
indices = list(range(l + 1))  # Indices of the shortest path

Spearman_rho_sq = np.zeros(l + 1)
Kendall_tau = np.array(range(l + 1))
Daniels_Guilbaud = np.zeros(l + 1)
sanity_check = np.zeros(l + 1)

cnt = 1
pi = copy.deepcopy(pi0)
for swap in swaps:
    pi[swap] = pi[swap[::-1]]
    Spearman_rho_sq[cnt] = calculate_S_sq(pi, pi0)
    Kendall_tau[cnt] = calculate_K(pi, pi0)
    Daniels_Guilbaud[cnt] = calculate_DG(pi, pi0)
    sanity_check[cnt] = n * Kendall_tau[cnt] - Daniels_Guilbaud[cnt]
    cnt += 1

plt.plot(indices, Spearman_rho_sq, 'r', indices, n * Kendall_tau, 'b', indices, Daniels_Guilbaud, 'g'
         , indices, sanity_check, 'm')
plt.legend(['Spearman_rho_sq', 'n*Kendall_tau', 'Daniels-Guilbaud', 'sanity_check'])
plt.show()
# plt.savefig("sanity.png", dpi=600)
