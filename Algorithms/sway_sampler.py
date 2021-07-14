from __future__ import division
from math import sqrt, exp
import random
import pdb
import itertools
import numpy as np
import time
from copy import deepcopy



def sway(pop, splitor, better, stop):
    """
    Args:
        pop: Candidate solutions
        splitor: SPLIT function
        better: BETTER function
        stop: Stopping population

    Returns:
        SWAY solutions
    """
    def cluster(items):
        N = len(items)

        # Termination condition
        if N < stop:
            return items
            #  end at here

        west, east, west_items, east_items = splitor(items)

        if better(east, west):
            selected = east_items
        if better(west, east):
            selected = west_items
        if not better(east, west) and not better(west, east):
            K = N // 2
            random_mask = np.array([1] * K + [0] * (N - K), dtype=bool)
            np.random.shuffle(random_mask)
            selected = items[random_mask]
        return cluster(selected)

    res = cluster(pop)

    return res
