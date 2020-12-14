# Deep Learning Models
---
This folder contains code for training Deep Learning (DL) models and the relevant results:

- ``DL-Q10000_dataset``: Part of the dataset for DL training. The optimal makespan of each JSSP instance is used as supervised training labels.
- ``model``: DL model training tf records, model checkpoints, and prediction with uncertainty.
- ``results``: JSSP benchmark results.
- ``utils``: Utilities for benchmarking.
- ``0_Trian_and_Predict_Q_Instances_with_Uncertainty.ipynb``: Train the DL model on JSSP instances and the optimal makespan and predict the optimal makespan with uncertainty.
- ``1_Benchmark_Runner_template.ipynb``: Templates for running ConvJSSP benchmark.
- ``2_Result_Parser.ipynb``: Example for parsing the ConvJSSP benchmark results.
- ``3_Result_Analysis.ipynb``: Example for analyzing the ConvJSSP benchmark results.
