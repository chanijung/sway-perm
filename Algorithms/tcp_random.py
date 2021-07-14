"""
Created on 2020/12/12
@author: nicklee

Python script for random permutation
"""
import os
import random


def tcp_random(dataset):
    path = 'Datasets/' + dataset + '/traces'
    # print(os.getcwd())
    file_list = os.listdir(path)
    # print(f'filelist: {file_list}')
    length = sum(['dump' in name for name in file_list])
    print(f'{dataset} {length}')

    # Randomly select a permutation
    x = list(range(1, length + 1))
    random.shuffle(x)

    return x

if __name__ == '__main__':
    for dataset in ["printtokens", "printtokens2", "schedule", "schedule2", "tcas", "totinfo"]:
        tcp_random(dataset)