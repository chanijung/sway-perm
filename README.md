# SWAY in Permutation Decision Space

This repository contains the artifact for the paper titled *Preliminary Evaluation of SWAY in Permutation Decision Space via a Novel Euclidean Embedding* by Junghyun Lee, Chani Jung, Yoo Hwa Park⋆, Dongmin Lee, Juyeon Yoon, and Shin Yoo, published at the 13th International Symposium on Search Based Software Engineering ([SSBSE 2021](https://conf.researchr.org/home/ssbse-2021)).

```
@inproceedings{Lee2021oo,
    author = {Junghyun Lee and Chani Jung and Yoo Hwa Park and Dongmin Lee and Juyeon Yoon and Shin Yoo},
    booktitle = {Proceedings of the 13th International Symposium on Search Based Software Engineering},
    series = {SSBSE 2021},
    title = {Preliminary Evaluation of SWAY in Permutation Decision Space via a Novel Euclidean Embedding},
    year = {2021}}
```

The paper extends [SWAY](https://ieeexplore.ieee.org/document/8249828), an efficient sampling based baseline search heuristic, to permutative decision space. The preliminary study uses Test Case Prioritisation (TCP) problem to study the feasibility of our theoretical extension, and this repository supports the replication of the study.

---
<!-- ## Instructions on running experiments
This has been tested successfully on the following test suites:
- flex
- grep
- gzip
- sed -->

## Replication

### Comparison of random, greedy, and SWAY
To reproduce results in Fig.2, run the following command:
```console
sh evaluate.sh
```

### Sensitivity test of SWAY to initial sample size
To reproduce results in Fig.3, run the following command:
```console
sh evaluate_initial.sh
```
