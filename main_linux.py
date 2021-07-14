"""
Created on 2020/12/14
@author: Dongmin1215, chanijung, yhpark, nicklee

(Description)
"""
from Algorithms.tcp_sway import *
from Algorithms.tcp_greedy import *

from Algorithms.get_apfd import *
from Algorithms.get_apsc import *

import os
import fileinput
import time
import argparse
from tqdm import tqdm
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # -d DATASET -n NUMBER -init INITIAL -s STOP -min MIN_Y -max MAX_Y
    parser.add_argument("-d", "--dataset", help="Name of subject program")
    parser.add_argument("-n", "--number", help="number of repetitions", type=int, default=30) 
    parser.add_argument("-init", "--initial", help="initial number of candidates", type=int, default=17) 
    parser.add_argument("-stop", "--stop", help="stop SWAY clustering when candidate number is less than this value",
                        type=int, default=100)
    parser.add_argument("-min", "--min_y", help="min value of y axis in box plot", type=float, default=0.5)
    parser.add_argument("-max", "--max_y", help="max value of y axis in box plot", type=float, default=1.0)

    args = parser.parse_args()
    dataset = args.dataset
    n = args.number

    # Dictionary of program_version: number_of_faults
    num_faults_dict = {
        'flex': {'1': 12, '2': 8, '3': 6, '4': 8, '5': 5},
        'grep': {'1': 3, '2': 1, '3': 5, '4': 3},
        'gzip': {'1': 7, '2': 3, '4': 3, '5': 4}, 'sed': {'2': 3, '3': 4}}
        
    # fault_matrices = {}
    test_dicts = {}
    suite = 1   # Fixed suite
    matrices, test_dict = fault_matrix_linux(dataset, suite, num_faults_dict)

    algs = ['SWAY', 'Additional Greedy', 'random']

    # Initial population
    init = 2 ** args.initial

    # Dict of program_name: list_of_version_numbers
    original_ver_dict = {'flex': ['1', '2', '3', '4'], 'grep': ['1', '2', '3'], 'gzip': ['1', '4'], 'sed': ['2']}
    
    # Dict of program_name: number_of_test_cases
    num_tests_dict = {'flex': 21, 'grep': 193, 'gzip': 211, 'sed': 36}

    #For each version of the subject program
    for ver in original_ver_dict[dataset]:
        apsc = np.zeros((3, n))
        apfd = np.zeros((3, n))
        runtime = np.zeros((3, n))

        # For each algorithm, solve TCP using APSC of previous version of the System Under Test (SUT).
        for i in tqdm(range(n)):

            # # Random algorithm
            start_time = time.time()
            res = list(range(1, num_tests_dict[dataset] + 1))
            random.shuffle(res)
            runtime[0][i] = time.time() - start_time

            apsc[0][i] = get_apsc_linux(dataset, suite, ver, res)
            apfd[0][i] = get_apfd(matrices[str(int(ver) + 1)],
                                    test_dict, dataset, None, res, True)

            # # Greedy algorithm
            start_time = time.time()
            res = tcp_greedy_linux(dataset, suite, ver)
            runtime[1][i] = time.time() - start_time

            apsc[1][i] = get_apsc_linux(dataset, suite, ver, res)
            apfd[1][i] = get_apfd(matrices[str(int(ver) + 1)],
                                    test_dict, dataset, None, res, True)

            # # # SWAY for TCP
            start_time = time.time()
            res, can = tcp_sway(dataset, suite, ver, init, args.stop)
            runtime[2][i] = time.time() - start_time

            tmp_apsc, tmp_apfd = [], []
            for perm in res:
                tmp_apsc.append(get_apsc_linux(dataset, suite, ver, perm))
                tmp_apfd.append(
                    get_apfd(matrices[str(int(ver) + 1)], test_dict, dataset, None, perm,
                                True))
            idx = tmp_apsc.index(max(tmp_apsc))
            apsc[2][i] = tmp_apsc[idx]
            apfd[2][i] = tmp_apfd[idx]

        apsc_mean = np.mean(apsc, axis=1)
        apsc_std = np.std(apsc, axis=1)
        apfd_mean = np.mean(apfd, axis=1)
        apfd_std = np.std(apfd, axis=1)

        print("apsc mean/std, APFD mean/std")
        print(f"random {dataset} s{suite} v{int(ver) + 1}: {apsc_mean[0]}/{apsc_std[0]}, {apfd_mean[0]}/{apfd_std[0]}")
        print(f"greedy {dataset} s{suite} v{int(ver) + 1}: {apsc_mean[1]}/{apsc_std[1]}, {apfd_mean[1]}/{apfd_std[1]}")
        print(f"sway {dataset} s{suite} v{int(ver) + 1}: {apsc_mean[2]}/{apsc_std[2]}, {apfd_mean[2]}/{apfd_std[2]}")

        # Save .csv
        # folder_name = "CSVs/CSV-(2^{})".format(args.initial)
        folder_name = "CSVs/CSV-test-(2^{})".format(args.initial)
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
        np.savetxt(folder_name + "/{}_s{}_v{}_apsc.csv".format(dataset, suite, int(ver) + 1), apsc, delimiter=",")
        np.savetxt(folder_name + "/{}_s{}_v{}_apfd.csv".format(dataset, suite, int(ver) + 1), apfd, delimiter=",")
        np.savetxt(folder_name + "/{}_s{}_v{}_runtime.csv".format(dataset, suite, int(ver) + 1), runtime, delimiter=",")
