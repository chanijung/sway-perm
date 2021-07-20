"""
Created on 2020/12/12
@author: chanijung, Dongmin1215, yhpark, nicklee
"""
import numpy as np
import pandas as pd

class APSCLinux(object):

    def __init__(self, dataset, suite, ver):
        self.path = path = 'Datasets/linuxutils/coverage_singlefault/' + dataset + '/s' + str(suite) + '/v' + ver + ".pkl"
        self.df = pd.read_pickle(self.path)

    # Assume that perm is a list of integers
    def get_apsc_linux(self, perm):
        """
        Args:
            perm: Permutation of test cases

        Returns:
            apsc
        """
        ts_values = []
        tc_order = 1
        uncovered_lines = []
        apsc=0
        for i in perm:  # i is test case number
            cov = self.df.iloc[:, i-1]
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