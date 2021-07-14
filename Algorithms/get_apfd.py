"""
Created on 2020/12/12
@author: nicklee, chanijung
"""

import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd



def fault_matrix_linux(dataset, suite, num_faults_dict):
    """
    Args:
        dataset: Name of subject program
        suite: Test suite ID number
        num_faults_dict: Dictionary that contains number of faults of each program version.

    Returns:
        fault matrix of size num_faults x num_tests
        dict of test case name: index
    """
    num_tests_dict = {'flex': {1: 21, 2: 525}, 'grep': {1: 193, 2: 152, 3: 140}, 'gzip': {1: 211},
                      'sed': {1: 36, 2: 360}}

    # Build test case map
    path = 'Datasets/linuxutils/coverage_singlefault/' + dataset + '/s' + str(suite)
    pkl_files = [f for f in listdir(path) if isfile(join(path, f)) and f[0] == 'v']
    pkl_files.sort()
    pkl = pkl_files[0]
    df = pd.read_pickle(path + "/" + pkl)
    tests = df.columns
    num_tests = num_tests_dict[dataset][suite]
    test_dict = {}
    for i in range(num_tests):
        test_dict[tests[i]] = i     # Maps the serial number and the exact name of testcases.

    # Build fault matrices
    path = 'Datasets/linuxutils/failing_tests_singlefault/' + dataset + '/s' + str(suite)
    dump_files = [f for f in listdir(path) if isfile(join(path, f)) and f[0] == 'v']
    dump_files.sort()
    num_faults = len(dump_files)
    matrices = {}
    for ver in num_faults_dict[dataset].keys():
        matrix = np.zeros([num_tests, num_faults_dict[dataset][ver]])
        matrices[ver] = matrix

    ##Fill in the matrices
    fault_count = 0
    ver = '0'
    for i in range(num_faults):
        dump = dump_files[i]
        if dump[1] != ver:
            fault_count = 0
        ver = dump[1]
        f = open(path + "/" + dump, "r", encoding="ISO-8859-1")
        for l in f.readlines():
            test = l.strip()
            if test_dict.get(test) == None:
                print(f'keyerror with {test} : {dataset} s{suite} ver{ver} ')
            matrices[ver][test_dict[test]][fault_count] = 1     # 0 or 1 for certain pair of testcase and fault
        fault_count += 1

    return matrices, test_dict


def get_apfd(matrix, test_dict, dataset, suite, perm, isLinux=False):
    """
    Args:
        matrix: Fault matrix
        test_dict: Dict of test case name: serial number
        dataset: Name of subject program
        suite: Test suite ID number
        isLinux: Is linux utility or not

    Returns:
        apfd
    """
    num_cases = matrix.shape[0]
    num_faults = matrix.shape[1]
    TFs = np.zeros(num_faults)  # Indices of the first test case that covers each fault

    if isLinux:
        test_suite = perm
        i = 1
        for case in test_suite:
            if np.prod(TFs) > 0:
                break
            for j in range(num_faults):
                if TFs[j] == 0 and matrix[case - 1][j] != 0:
                    TFs[j] = i
                    # print(f'TFs[{j}] = {i}')
            i += 1

    apfd = 1 - sum(TFs) / (num_cases * num_faults) + 0.5 / num_cases

    return apfd
