"""
Created on 2020/12/12
@author: Dongmin1215, chanijung, yhpark, nicklee

Python script for reproducing the results
"""

from __future__ import division

import sys
import os
from Algorithms.sway_sampler import sway
from Algorithms.get_apsd import *
from multiprocessing import Pool
import numpy as np
from numpy import linalg as LA
import bisect  # Python module for sorted list
from functools import partial
import time


def rank_vector(pi):
    n = len(pi)
    result = np.zeros(n)

    for i in range(n):
        # result[i] = pi.index(i + 1)
        result[i] = np.where(pi == i + 1)[0][0]
    return result


def dist(ind1, ind2):
    ind1 = rank_vector(ind1)  # To calculate swap distance
    ind2 = rank_vector(ind2)
    return LA.norm(ind1 - ind2)


def farthest_from(pop, pivot):  # pop = numpy matrix of candidates
    result = pop[0]
    distance = dist(result, pivot)
    length = len(pop)
    for i in range(1, length):
        tmp = pop[i]
        new_distance = dist(tmp, pivot)
        if new_distance > distance:
            result = tmp
            distance = new_distance
    return result


def where(pop):  # pop = numpy matrix of candidates
    # print(pop.shape)
    # time.sleep(5)

    ## Random pivot
    rand = pop[np.random.randint(0, len(pop))]
    # rand = pop[0]

    ## east (farthest from pivot)
    east = farthest_from(pop, rand)
    # ds = [dist(i, rand) for i in pop]
    # east = pop[ds.index(max(ds))]

    ## west (farthest from east)
    west = farthest_from(pop, east)
    # ds = [dist(i, east) for i in pop]
    # west = pop[ds.index(max(ds))]

    ## cosine rule
    c = dist(east, west)
    cc = 2 * c ** 0.5
    # print(east)
    # print(west)
    # print(pop)
    # time.sleep(5)
    # if cc == 0:
    #     print(east)
    #     print(west)
    #     print(pop)
    assert (cc > 0)

    mappings = list()
    num_pops = len(pop)
    # for x in pop:
    for i in range(num_pops):
        x = pop[i]
        a = dist(x, west)
        b = dist(x, east)
        d = (a + c - b) / cc
        bisect.insort(mappings, (d, i))
        # mappings.append((x, d))

    # mappings = sorted(mappings, key=lambda i: i[1])
    mappings = np.array([pop[mappings[i][1]] for i in range(num_pops)])

    n = len(mappings)
    # eastItems = np.concatenate((mappings[:int(n * 0.2)], mappings[int(n * 0.5):int(n * 0.8)]))
    # westItems = np.concatenate((mappings[int(n * 0.2):int(n * 0.5)], mappings[int(n * 0.8):]))
    eastItems = mappings[:int(n * 0.5)]
    westItems = mappings[int(n * 0.5):]
    # eastItems = mappings[:int(n * 0.2)] + mappings[int(n * 0.5):int(n * 0.8)]
    # westItems = mappings[int(n * 0.2):int(n * 0.5)] + mappings[int(n * 0.8):]

    return west, east, eastItems, westItems


def permute_row(seed, i):
    # return np.random.permutation(seed)
    return np.random.RandomState(seed=np.random.randint(1e7)).permutation(seed)


def tcp_sway(dataset, suite, ver, initial, stop, alg=2):
    # num_tests_dict = {'flex':21, 'grep':193, 'gzip':211, 'sed':36}
    num_tests_dict = {'flex': {1: 21, 2: 525}, 'grep': {1: 193, 2: 152, 3: 140}, 'gzip': {1: 211},
                      'sed': {1: 36, 2: 360}}

    # Compare function
    def comparing(part1, part2):  ##Need modification
        if ver == '0':
            return get_apsd(dataset, part1) > get_apsd(dataset, part2)
        else:
            return get_apsd_linux(dataset, suite, ver, part1) > get_apsd_linux(dataset, suite, ver, part2)

    if ver == '0':
        path = 'Datasets/' + dataset + '/traces'
        file_list = os.listdir(path)
        length = sum(['dump' in name for name in file_list])
    else:  # linux utils
        length = num_tests_dict[dataset][suite]

    ## Build initial population in a parallel manner
    seed = np.array(range(1, length + 1))
    wrapper = partial(permute_row, seed)
    pool = Pool()
    new_rows = pool.map(wrapper, range(1, initial))
    pool.close()
    candidates = np.concatenate((np.reshape(seed, (1, length)), np.array(new_rows)))
    # candidates = []
    # for _ in range(initial):
    #     x = list(range(1, length + 1))
    #     while x in candidates:  # avoid any repetitions
    #         random.shuffle(x)
    #     candidates.append(x)

    ## Binary embedding
    if alg == 1:
        raise ValueError("Binary embedding not yet implemented!!")
        # emb_cand, emb_dict = embed(candidates)
        # res = sway(emb_cand, partial(split_products, groupC=min(15, dim // 7)), comparing, alg, emb_dict)
        # return res, candidates

    ## Continuous embedding
    elif alg == 2:
        return sway(candidates, where, comparing, stop, alg, None), candidates
