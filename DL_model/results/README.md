# Results

The experiments for solving the JSSP instances in the test set are performed on a machine with the following specification:
- CPU: Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz
- Memory: 4 × 4 GB DDR3 1600 MHz
- Operating System: Ubuntu 18.04.4 LTS
- Kernel: Linux 5.3.0-45-generic
Note that [Turbo Boost](https://www.intel.com/content/www/us/en/architecture-and-technology/turbo-boost/turbo-boost-technology.html) has been turned off on the machine for reproducibility

We implement all the CP programs using [Gecode](https://github.com/Gecode/gecode) 6.2.0. Gecode natively provides multi-threading to speed up the solution finding process, however, in all of our benchmark of comparing different strategies to find optimal makespan, we use a single thread, because we use the execution time as a surrogate for the computation cost, thus, the extra speed up brought by multi-threading complicates the measurement of computation of the problem.