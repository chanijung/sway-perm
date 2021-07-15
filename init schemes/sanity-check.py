"""
Created on 2021/03/29
@author: nicklee

Check whether the theorem (Monjardet, 1998) is correct, computationally
From randomly initialized permutation pi0, let pif be the permutation that is the farthest from pi0 w.r.t. swap distance
Consider a sequence of permutations that form the shortest path from pi0 to pif
"""
import matplotlib.pyplot as plt
from helper_funcs import *
import numpy as np
import copy

if __name__ == '__main__':
    n = 20  # Size of permutation

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

    # Compute each metric!
    cnt = 1
    pi = copy.deepcopy(pi0)
    for swap in swaps:
        pi[swap] = pi[swap[::-1]]
        Spearman_rho_sq[cnt] = calculate_S_sq(pi, pi0)
        Kendall_tau[cnt] = calculate_K(pi, pi0)
        Daniels_Guilbaud[cnt] = calculate_DG(pi, pi0)
        sanity_check[cnt] = n * Kendall_tau[cnt] - Daniels_Guilbaud[cnt]
        cnt += 1

    # Plot metric(pi0, pi) for all considered pi's
    plt.plot(indices, Spearman_rho_sq, 'r', indices, n * Kendall_tau, 'b', indices, Daniels_Guilbaud, 'g'
             , indices, sanity_check, 'm')
    plt.legend(['Spearman_rho_sq', 'n*Kendall_tau', 'Daniels-Guilbaud', 'sanity_check'])
    plt.title('Checking that Theorem 1 (Monjardet, 1998) is correct...')
    plt.xlabel('Index of the sequence of permutations forming the shortest path from pi0 to pif')
    plt.show()
    # plt.savefig("sanity.png", dpi=600)
