# SWAY in Permutation Decision Space
Code for the paper *Preliminary Evaluation of SWAY in Permutation Decision Space via a Novel Euclidean Embedding*.
> Junghyun Lee, Dongmin Lee, Chani Jung, and Yoo Hwa Park
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
sh total_plot_linux.sh
```

### Sensitivity of SWAY to initial sample size
To reproduce results in Fig.3, run the following command:
```console
sh total_plot_linux_init.sh
```

---
## To-Do
- [ ] Currently, there are unparsable characters that we've preprocessed out (e.g. "["-->"0"). Is there some way to not do this and still run the experiments?
  (Due to this issue, replace cannot be tested.)
- [ ] Automate the running experiments section using shell script
- [ ] Extend the support of this to non-Siemens test suites (ex. space, sed)
- [ ] Implement genetic algorithm-based TCP to be compared with our SWAY-based approach
- [ ] Fix arg parsing to be more "robust"
- [ ] Fix mts.jar for other test suites...