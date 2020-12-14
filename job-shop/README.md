# Job-Shop Scheduling Problems

---

This folder holds the C++ code of different approaches for solving (finding the optimal makespan) JSSP problems. 
- Job-shop Scheduling Problems (JSSPs)
- [Gecode](https://www.gecode.org/) is selected as the tool for the Constraint Programming (CP) part. 
- See 2.6.1 of [Modeling and Programming with Gecode](https://www.gecode.org/doc-latest/MPG.pdf) for a detailed Gecode installation guide.


## Code
---

### JSSP Solvers
- ''job-shop-baseline.cpp'' 
    - This file holds the baseline code for JSSP from [here](https://github.com/chschulte/gecode/blob/job-shop-experiments/examples/job-shop.cpp). Some extra comments are added to help better understand the code.

- ''job-shop-naive.cpp'' Note this is the ``greedy strategy`` in the paper. 
    - This file holds the code for a naive approach for solving JSSP. The approach works as follows: 
        - Take **p = pred_optimal_makespan** as an extra input to the program;
        - Try **p**, if succeed, **p=p-1**, else, **p=p+1**. 
        - Stopping criterion:
            - if prev==True and cur==False, report **p+1** as optimal;
            - if prev==False and cur==True, report **p** as optimal;
            - otherwise, continue.

- ''job-shop-hybrid-baseline-jump-half-naive.cpp''
	- The only difference between this program and the ``job-shop-baseline.cpp`` program is that after the probing phase, we perform one check on whether the **predicted_optimal_makespan** is within the lower_bound and upper_bound found after the probing phase:
		- if so,  jump(half), while we are moving in one direction, then naive(greedy);
		- otherwise, ignore the prediction and continue with the baseline model.

- ''job-shop-hybrid-baseline-jump-half-exhaustive-search.cpp''
	- The only difference between this program and the ``job-shop-baseline.cpp`` program is that after the probing phase, we perform one check on whether the **predicted_optimal_makespan** is within the lower_bound and upper_bound found after the probing phase:
		- if so,  jump(half), while we are moving in one direction, then exhaustive-search;
		- otherwise, ignore the prediction and continue with the baseline model.

- ''job-shop-hybrid-baseline-jump-std-naive.cpp''
	- The only difference between this program and the ``job-shop-baseline.cpp`` program is that after the probing phase, we perform one check on whether the **predicted_optimal_makespan** is within the lower_bound and upper_bound found after the probing phase:
		- if so,  jump(std), while we are moving in one direction, then naive(greedy);
		- otherwise, ignore the prediction and continue with the baseline model.

- ''job-shop-hybrid-baseline-jump-std-exhaustive-search.cpp''
	- The only difference between this program and the ``job-shop-baseline.cpp`` program is that after the probing phase, we perform one check on whether the **predicted_optimal_makespan** is within the lower_bound and upper_bound found after the probing phase:
		- if so,  jump(std), while we are moving in one direction, then exhaustive-search;
		- otherwise, ignore the prediction and continue with the baseline model.

### JSSP Instances
- ''job-shop-instances.hpp''
    - This file holds the JSSP instances that is already used for the experiments.
	- ``Instance-Q10000`` dataset: 10000 randomly generated 9x9 JSSP instances (q0000 ~ q9999)

### Utilities
- ''Makefile''
    - This file holds the MAKEFILE for compiling the experimentation code. Node Gecode is needed.
- ''job-shop-generate.cpp''
    - This file holds the code for generating JSSP instances needed for the experiments.

## Example of baseline solver
---
```
 % ./job-shop-baseline q9210
	Probing...
		Bounds: [568,4181]
		q9210 [makespan: 975]
		q9210 [makespan: 919]
		q9210 [makespan: 914]
		q9210 [makespan: 881]
			nodes:      12246
			failures:   3
			peak depth: 542
			runtime:    0.208 (208.096 ms)

	Adjusting...
		Bounds: [568,881]
		Bounds: [725,881]
		Bounds: [804,881]
		q9210 [makespan: 840]
		Bounds: [804,840]
		Bounds: [823,840]
		q9210 [makespan: 830]
		Bounds: [823,830]
		q9210 [makespan: 825]
		Bounds: [823,825]
			nodes:      435144
			failures:   217311
			restarts:   15
			no-goods:   216
			peak depth: 100
			runtime:    30.000 (30000.076 ms)
		stopped due to time-out...

	Solving...
			nodes:      322477
			failures:   161162
			restarts:   9
			no-goods:   124
			peak depth: 73
			runtime:    21.840 (21840.815 ms)

	Found best solution and proved optimality.
```