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
    parser.add_argument("-d", "--dataset", help="dataset name")
    parser.add_argument("-n", "--number", help="number of repetitions", type=int, default=30) 
    parser.add_argument("-init", "--initial", help="initial number of candidates", type=int, default=18) 
    parser.add_argument("-stop", "--stop", help="stop SWAY clustering when candidate number is less than this value",
                        type=int, default=100)
    parser.add_argument("-min", "--min_y", help="min value of y axis in box plot", type=float, default=0.5)
    parser.add_argument("-max", "--max_y", help="max value of y axis in box plot", type=float, default=1.0)

    args = parser.parse_args()
    dataset = args.dataset
    n = args.number

    num_faults_dict = {
        'flex': {1: {'1': 12, '2': 8, '3': 6, '4': 8, '5': 5}},
        'grep': {1: {'1': 3, '2': 1, '3': 5, '4': 3}},
        'gzip': {1: {'1': 7, '2': 3, '4': 3, '5': 4}}, 'sed': {1: {'2': 3, '3': 4}}}
        
    suites = num_faults_dict[dataset].keys()
    fault_matrices = {}
    test_dicts = {}
    for suite in suites:
        matrices, test_dict = fault_matrix_linux(dataset, suite, num_faults_dict)
        fault_matrices[suite] = matrices
        test_dicts[suite] = test_dict

    algs = ['SWAY', 'Additional Greedy', 'random']

    # Initial population
    init = 2 ** args.initial

    original_ver_dict = {'flex': ['1', '2', '3', '4'], 'grep': ['1', '2', '3'], 'gzip': ['1', '4'], 'sed': ['2']}
    num_tests_dict = {'flex': {1: 21, 2: 525}, 'grep': {1: 193, 2: 152, 3: 140}, 'gzip': {1: 211},
                      'sed': {1: 36, 2: 360}}

    for ver in original_ver_dict[dataset]:
        for suite in suites:
            apsc = np.zeros((3, n))
            apfd = np.zeros((3, n))
            runtime = np.zeros((3, n))

            if dataset == 'grep' and suite == 3 and ver == '3':  # data omitted
                continue

            # For each algorithm, solve TCP using APSC computed from the previous version of the System Under Test (SUT).
            for i in tqdm(range(n)): # TCP for the (ver+1)th program version

                # # Random algorithm
                print(f'random')
                start_time = time.time()
                res = list(range(1, num_tests_dict[dataset][suite] + 1))
                random.shuffle(res)
                runtime[0][i] = time.time() - start_time

                apsc[0][i] = get_apsc_linux(dataset, suite, ver, res)
                apfd[0][i] = get_apfd(fault_matrices[suite][str(int(ver) + 1)],
                                      test_dicts[suite], dataset, None, res, True)

                # # Greedy algorithm
                print("greedy")
                start_time = time.time()
                res = tcp_greedy_linux(dataset, suite, ver)
                runtime[1][i] = time.time() - start_time

                apsc[1][i] = get_apsc_linux(dataset, suite, ver, res)
                apfd[1][i] = get_apfd(fault_matrices[suite][str(int(ver) + 1)],
                                      test_dicts[suite], dataset, None, res, True)

                # # # SWAY for TCP
                print(f'sway')
                start_time = time.time()
                res, can = tcp_sway(dataset, suite, ver, init, args.stop)
                runtime[2][i] = time.time() - start_time
                print(f'sway {time.time() - start_time} taken')

                tmp_apsc, tmp_apfd = [], []
                for perm in res:
                    tmp_apsc.append(get_apsc_linux(dataset, suite, ver, perm))
                    tmp_apfd.append(
                        get_apfd(fault_matrices[suite][str(int(ver) + 1)], test_dicts[suite], dataset, None, perm,
                                 True))
                idx = tmp_apsc.index(max(tmp_apsc))
                apsc[2][i] = tmp_apsc[idx]
                apfd[2][i] = tmp_apfd[idx]

            apsc_mean = np.mean(apsc, axis=1)
            apsc_std = np.std(apsc, axis=1)
            apfd_mean = np.mean(apfd, axis=1)
            apfd_std = np.std(apfd, axis=1)

            print("apsc mean/std, APFD mean/std")
            print(f"random {dataset} s{suite} v{ver}: {apsc_mean[0]}/{apsc_std[0]}, {apfd_mean[0]}/{apfd_std[0]}")
            print(f"greedy {dataset} s{suite} v{ver}: {apsc_mean[1]}/{apsc_std[1]}, {apfd_mean[1]}/{apfd_std[1]}")
            print(f"sway {dataset} s{suite} v{ver}: {apsc_mean[2]}/{apsc_std[2]}, {apfd_mean[2]}/{apfd_std[2]}")

            # Save .csv
            # folder_name = "CSVs/CSV-(2^{})".format(args.initial)
            folder_name = "CSVs/CSV-test-(2^{})".format(args.initial)
            if not os.path.isdir(folder_name):
                os.makedirs(folder_name)
            np.savetxt(folder_name + "/{}_s{}_v{}_apsc.csv".format(dataset, suite, ver), apsc, delimiter=",")
            np.savetxt(folder_name + "/{}_s{}_v{}_apfd.csv".format(dataset, suite, ver), apfd, delimiter=",")
            np.savetxt(folder_name + "/{}_s{}_v{}_runtime.csv".format(dataset, suite, ver), runtime, delimiter=",")
