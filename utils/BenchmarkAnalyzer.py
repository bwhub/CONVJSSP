import pathlib
import collections
import nltk
import numpy as np
import pandas as pd

# The bench mark analyzer is made to analyze logs starting with the following name.
# branching_afc_timeadjust_30000_timeprobe_1000_timesolve_0_q0001_run_0.log


class BenchmarkAnalyzer:
    def __init__(self, log_folder='logs', suffix='.log'):
        # a default dictionary that holds the raw benchmark result as str
        self._benchmark_result_dict = collections.defaultdict(dict)
        self._log_folder = log_folder
        self._required_suffix = suffix
        
        self._read_log_files()
        print("Finish reading {0} benchmarking logs.".format(len(self._benchmark_result_dict)))
        self._parse_raw_str()
        print("Finish parsing the logs")
        
        self._benchmark_result_pd = self._construct_pandas_df()
        print("Finish constructing pandas dataframe.")
        
    def _read_log_files(self, overwrite=True):
        if overwrite:
            self._benchmark_result_dict.clear()
        
        log_dir_path = pathlib.Path.cwd().joinpath(self._log_folder)
        # ''log_names'' is a sorted list of names of all the log files to be analyzed
        log_names = sorted([log for log in log_dir_path.iterdir()])
        for single_log in log_names:
            # print(single_log.stem)
            # print(single_log.stem.rsplit('_'))
            if single_log.suffix == self._required_suffix:
                with open(single_log, 'r') as inputFile:
                    name_split_list = single_log.stem.rsplit('_')
#                     key = [name_split_list[-3], name_split_list[1], name_split_list[3]]
                    key = [name_split_list[-3], name_split_list[1], '0.00']
                    # key = [q0001, afc, 0.00]
                    self._benchmark_result_dict[tuple(key)]['raw_str'] = inputFile.read()
 
    def _parse_raw_str(self):
        for key in self._benchmark_result_dict:
            single_log_list = nltk.word_tokenize(self._benchmark_result_dict[key]['raw_str'])
            # print(single_log_list)
            self._benchmark_result_dict[key]['runtime_ms'] = self._calculate_running_time_for_one_log(single_log_list)
            self._benchmark_result_dict[key]['makespan'] = self._get_makespan_list_for_one_log(single_log_list)
            self._benchmark_result_dict[key]['probing_makespan'] = self._get_makespan_list_for_one_log(nltk.word_tokenize(self._benchmark_result_dict[key]['raw_str'].split("Adjusting...")[0]))
            self._benchmark_result_dict[key]['bound'] = self._get_bound_list_for_one_log(single_log_list)
            self._benchmark_result_dict[key]['running_cmd'] = self._benchmark_result_dict[key]['raw_str'].split('\n')[0]


    
    # def _calculate_running_time_for_one_log(self, single_log_list):
    #     print(single_log_list)
    #     result = [float(single_log_list[ind+4]) for ind, val in enumerate(single_log_list) if val == 'runtime']
    #     while len(result) < 3:
    #         result.append(0)
    #     return result

    def _calculate_running_time_for_one_log(self, single_log_list):
        # print(single_log_list)
        result = [float(single_log_list[ind-1]) for ind, val in enumerate(single_log_list) if val == 'ms']
        while len(result) < 3:
            result.append(0)
        return result
    
    def _get_makespan_list_for_one_log(self, single_log_list):
        return [int(single_log_list[ind+2]) for ind, val in enumerate(single_log_list) if val == 'makespan']
    
    def _get_bound_list_for_one_log(self, single_log_list):
        return [tuple(single_log_list[ind+3].split(',')) for ind, val in enumerate(single_log_list) if val == 'Bounds']


    def _construct_pandas_df(self):
        # this function construct a pandas dataframe from the content in self._benchmark_result_dict
        rows_list = []
        for key, val in self._benchmark_result_dict.items():
            temp_dict = {}
            temp_dict['Instance'] = str(key[0])
            temp_dict['Heuristic'] = str(key[1])
            temp_dict['tbf'] = float(key[2])
            temp_dict['probing_time_ms'] = float(val['runtime_ms'][0])
            temp_dict['adjusting_time_ms'] = float(val['runtime_ms'][1])
            temp_dict['solving_time_ms'] = float(val['runtime_ms'][2])
            temp_dict['runtime_ms'] = float(np.sum(val['runtime_ms']))
            # temp_dict['makespan'] = float(np.min(val['makespan']))
            temp_dict['makespan'] = float(val['makespan'][-1])
            temp_dict['first_LB'] = int(val['bound'][0][0])
            temp_dict['first_UB'] = int(val['bound'][0][1])
            # temp_dict['first_makespan'] = int(val['makespan'][0])
            # temp_dict['probing_progress'] = float((val['probing_makespan'][0] - val['probing_makespan'][-1])/val['probing_makespan'][0])
            temp_dict['running_cmd'] = val['running_cmd']

            rows_list.append(temp_dict)

        return pd.DataFrame(rows_list)
    
    def get_result_df(self, condition=None):
        if condition == None:
            return self._benchmark_result_pd
        return self._benchmark_result_pd.loc[self._benchmark_result_pd["Instance"].str.startswith(condition)]
    
    def get_result_dict(self, condition=None):
        benchmark_result_df = self.get_pandas_df(condition)
        return dict([x for x in benchmark_result_df.groupby('Instance', sort=False)])