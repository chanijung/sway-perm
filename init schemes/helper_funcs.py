"""
Created on 2021/07/15
@author: nicklee

Helper functions for computing permutation distances
"""
import numpy as np


def compare(pi, pi0):
    """

    Args:
        pi: current permutation
        pi0: initial permutation

    Returns: True if they are the same, False otherwise

    """
    return np.prod(pi == pi0)


# ToDo: Change to numpy implementation
def extract(pi, S):
    """

    Args:
        pi: permutation
        S: subset of [n], which should be thought of indices of pi

    Returns: order restriction of pi (as linear oder) to S

    """
    result = []

    for item in pi:
        if item in S:
            result.append(item)

    assert (len(result) == len(S))
    return np.array(result)


def calculate_DG(pi, pi0):
    """

    Args:
        pi: current permutation
        pi0: initial permutation

    Returns: d_G(pi, pi0) i.e. Daniels-Guilbard distance of pi and pi0

    """
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
    """

    Args:
        pi: current permutation
        pi0: initial permutation

    Returns: d_K(pi, pi0) i.e. Kendall-tau distance of pi and pi0

    """
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
    """

    Args:
        pi: current permutation

    Returns: rank permutation (as a vector)

    """
    pi = list(pi)
    n = len(pi)
    result = []

    for i in range(n):
        result.append(pi.index(i))

    return np.array(result)


def calculate_S_sq(pi, pi0):
    """

    Args:
        pi: current permutation
        pi0: initial permutation

    Returns: d_S(pi, pi0) i.e. Spearman-rho distance of pi and pi0

    """
    r = rank_vector(pi)
    r0 = rank_vector(pi0)

    return np.linalg.norm(r - r0) ** 2
