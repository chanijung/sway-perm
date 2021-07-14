# SWAY in Permutation Decision Space
Code for the paper *Preliminary Evaluation of SWAY in Permutation Decision Space via a Novel Euclidean Embedding*.
> Junghyun Lee, Chani Jung, Dongmin Lee, and Yoo Hwa Park
> 
> 
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

---
## To-Do
- [ ] Implement genetic algorithm-based TCP to be compared with our SWAY-based approach
- [ ] Fix arg parsing to be more "robust"re