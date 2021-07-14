"""
Created on 2020/12/12
@author: chanijung, Dongmin1215, yhpark, nicklee
"""
import numpy as np
import pandas as pd



# Assume that perm is a list of integers
def get_apsc_linux(dataset, suite, ver, perm):
    """
    Args:
        dataset: Name of subject program
        suite: Test suite ID number
        ver: Subject program version number
        perm: Permutation of test cases

    Returns:
        apsc
    """
    ts_values = []
    tc_order = 1
    uncovered_lines = []
    path = 'Datasets/linuxutils/coverage_singlefault/' + dataset + '/s' + str(suite) + '/v' + ver + ".pkl"
    df = pd.read_pickle(path)
    apsc=0
    for i in perm:  # i is test case number
        cov = df.iloc[:, i-1]
        profile = np.array(cov!=0).astype(int)
        if tc_order == 1:
            uncovered_lines = list(range(profile.size))
        for k in uncovered_lines:  # j is line number
            bit = profile[k]
            if bit:
                ts_values.append(tc_order)
                uncovered_lines.remove(k)  # Will not check the cover of this line anymore
        tc_order += 1

    apsc = 1 - sum(ts_values) / ((tc_order - 1) * profile.size) + 0.5 / (tc_order - 1)

    return apsc
