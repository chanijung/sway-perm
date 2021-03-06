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

## Reproducing results in the paper

### Correlations between swap(Kendall-tau) distance and different embedding distances
<img src="https://user-images.githubusercontent.com/17661005/125710625-1d8aabc7-fe66-49e6-b652-8c45acf0d43d.png" width="350"/> <img src="https://user-images.githubusercontent.com/17661005/125710961-f1008bff-6b02-44a0-89ba-a8194cda0152.png" width="350"/>
<!-- ![](https://user-images.githubusercontent.com/17661005/125710625-1d8aabc7-fe66-49e6-b652-8c45acf0d43d.png) ![](https://user-images.githubusercontent.com/17661005/125710961-f1008bff-6b02-44a0-89ba-a8194cda0152.png) -->

This is the main (empirical) motivation for a new embedding of permutation decision space: note how the Kendall tau has no correlation with the naive embedding's Euclidean distance! Using our proposed embedding, one can retain an almost perfect correlation with the Kendall tau.

To reproduce results in Fig. 1, run the following command *in "init schemes" folder*:

```console
python reproduce-fig1.py
```

<br/>

### Comparison of random, greedy, and SWAY algorithms for TCP on Linux programs
<img src="https://user-images.githubusercontent.com/46154572/125720279-0e6b16de-3e21-48b8-996e-34313bcfa374.png" width="350"/> <img src="https://user-images.githubusercontent.com/46154572/125720298-d4b95c46-febb-446f-88cd-910c9671073c.png" width="350"/>
<!-- ![](https://user-images.githubusercontent.com/46154572/125720279-0e6b16de-3e21-48b8-996e-34313bcfa374.png) ![](https://user-images.githubusercontent.com/46154572/125720298-d4b95c46-febb-446f-88cd-910c9671073c.png) -->
To reproduce results in Fig.2, run the following command:
```console
sh evaluate.sh
```
<br/>

### Sensitivity of SWAY to initial population size
<img src="https://user-images.githubusercontent.com/46154572/125720301-9a672f4e-fd36-4948-90da-436dd4a531d5.png" width="350"/> <img src="https://user-images.githubusercontent.com/46154572/125720305-bdfcdbc6-00ca-4dcd-b061-f2ad6db2d732.png" width="350"/>
<!-- ![](https://user-images.githubusercontent.com/46154572/125720301-9a672f4e-fd36-4948-90da-436dd4a531d5.png) ![](https://user-images.githubusercontent.com/46154572/125720305-bdfcdbc6-00ca-4dcd-b061-f2ad6db2d732.png) -->
To reproduce results in Fig.3, run the following command:
```console
sh evaluate_initial.sh
```

