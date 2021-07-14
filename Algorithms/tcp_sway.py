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
    ## Random pivot
    rand = pop[np.random.randint(0, len(pop))]
    east = farthest_from(pop, rand)
    west = farthest_from(pop, east)

    ## cosine rule
    c = dist(east, west)
    cc = 2 * c ** 0.5
    assert (cc > 0)

    mappings = list()
    num_pops = len(pop)
    for i in range(num_pops):
        x = pop[i]
        a = dist(x, west)
        b = dist(x, east)
        d = (a + c - b) / cc
        bisect.insort(mappings, (d, i))

    mappings = np.array([pop[mappings[i][1]] for i in range(num_pops)])

    n = len(mappings)
    eastItems = mappings[:int(n * 0.5)]
    westItems = mappings[int(n * 0.5):]

    return west, east, eastItems, westItems


def permute_row(seed, i):
    return np.random.RandomState(seed=np.random.randint(1e7)).permutation(seed)


def tcp_sway(dataset, suite, ver, initial, stop):
    num_tests_dict = {'flex': {1: 21, 2: 525}, 'grep': {1: 193, 2: 152, 3: 140}, 'gzip': {1: 211},
                      'sed': {1: 36, 2: 360}}

    # Compare function
    def comparing(part1, part2):
        return get_apsd_linux(dataset, suite, ver, part1) > get_apsd_linux(dataset, suite, ver, part2)

    length = num_tests_dict[dataset][suite]

    ## Build initial population in a parallel manner
    seed = np.array(range(1, length + 1))
    wrapper = partial(permute_row, seed)
    pool = Pool()
    new_rows = pool.map(wrapper, range(1, initial))
    pool.close()
    candidates = np.concatenate((np.reshape(seed, (1, length)), np.array(new_rows)))

    return sway(candidates, where, comparing, stop, None), candidates
