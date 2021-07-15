"""
Created on 2021/03/29
@author: nicklee

Reproduce figure 1 in the paper i.e. check the correlation with Spearman rho distance and other distances
"""
import matplotlib.pyplot as plt
from helper_funcs import *


def calculate_naive(pi, pi0):
    """

    Args:
        pi: current permutation
        pi0: initial permutation

    Returns: Euclidean distance of pi and pi0, with naive embedding!

    """
    return np.linalg.norm(pi - pi0) ** 2


if __name__ == '__main__':
    repeats = 1000
    n = 20

    Spearman_rho_sq = np.zeros(repeats)
    Euclidean_naive = np.zeros(repeats)
    Kendall_tau = np.zeros(repeats)
    Daniels_Guilbaud = np.zeros(repeats)

    for i in range(repeats):
        pi = np.random.permutation(n)
        pi_ = np.random.permutation(n)

        Spearman_rho_sq[i] = calculate_S_sq(pi, pi_)
        Euclidean_naive[i] = calculate_naive(pi, pi_)
        Kendall_tau[i] = calculate_K(pi, pi_)
        Daniels_Guilbaud[i] = calculate_DG(pi, pi_)

    # Plot!
    plt.figure(1)
    plt.scatter(Spearman_rho_sq, Kendall_tau)
    plt.title('Kendall tau vs Spearman rho')
    plt.xlabel('Spearman rho distance')
    plt.ylabel('Kendall tau distance')

    plt.figure(2)
    plt.scatter(Euclidean_naive, Kendall_tau)
    plt.title('Kendall tau vs Euclidean(naive)')
    plt.xlabel('Euclidean distance (naive embedding)')
    plt.ylabel('Kendall tau distance')

    plt.figure(3)
    plt.scatter(Spearman_rho_sq, Daniels_Guilbaud)
    plt.title('Kendall tau vs Daniels-Guilbaud')
    plt.xlabel('Daniels-Guilbaud distance')
    plt.ylabel('Kendall tau distance')

    plt.show()
