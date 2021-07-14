"""
Created on 2020/12/12
@author: chanijung
"""
import numpy as np
import random
from os import listdir
from os.path import isfile, join
import pandas as pd


def tcp_greedy_linux(dataset, suite, ver):
    """
    Args:
        dataset: Name of System Under Test (SUT)
        suite: Test suite ID number
        ver: SUT version number

    Returns:
        TCP greedy solution of test suite size
    """
    path = 'Datasets/linuxutils/coverage_singlefault/' + dataset + '/s' + str(suite) + '/v' + ver + ".pkl"
    df = pd.read_pickle(path)
    mat = np.transpose(df.to_numpy())
    mat = (mat>0).astype(int)
    complete_mat = np.copy(mat)

    num_tests = mat.shape[0]

    sol = []
    remaining = np.array(range(num_tests))
    while True:
        # Find TCP solution with greedy algorithm until full coverage
        sol += list(remaining[greedy_until_full_cov(mat)])
        remaining = np.array(list(set(range(num_tests)) - set(sol)))
        if remaining.size==0:
            break
        mat = complete_mat[remaining,:]

    return [i+1 for i in sol]


# Find TCP solution with greedy algorithm until full coverage is accomplished.
def greedy_until_full_cov(mat):
    """
    Args:
        mat: Coverage matrix of test cases

    Returns:
        TCP greedy solution until full coverage is accomplished
    """
    sol = []
    num_tests = mat.shape[0]
    num_valid_stats = mat.shape[1]
    covered_stats = np.zeros((1, num_valid_stats))

    for _ in range(num_tests):
        addit_stats = (mat - covered_stats == 1).astype(int)
        addit_cov = np.sum(addit_stats, axis=1)
        if np.sum(addit_cov) == 0:
            break
        next_test = np.argmax(addit_cov)
        covered_stats = (covered_stats + mat[next_test] > 0).astype(int)
        sol.append(next_test)

    return sol

