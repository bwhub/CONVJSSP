import subprocess
from tqdm import tqdm
import itertools as it
import os
import multiprocessing as mp

class BenchmarkRunner:
    def __init__(self, log_dir, exec_path="../src/job-shop-experiment/job-shop", repeat_time=1, warmup_seconds=0):
        self.exec_path = exec_path + " "
        self.log_dir = log_dir
        self.repeat_time = repeat_time
        self.available_parameter_dict, self.available_instance_list = self._get_avaialbe_benchmark_options()
        print("# Length of the available instance list is {}".format(len(self.available_instance_list)))
        self.test_parameter_dict = {}
        self.test_instance_list = []
        self.warmup_seconds = warmup_seconds
        # add testing parameters
        
    def _run_single_command(self, cmd_str):
        # function to execute a single command
        p = subprocess.Popen(cmd_str.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, err = p.communicate()
        return output.decode('utf-8')
    
    def run_test(self, log_dir=None):
        if log_dir==None:
            log_dir = self.log_dir
        all_parameter_names = sorted(self.test_parameter_dict)
        # all_parameter_names = self.test_parameter_dict
        parameter_combination_list = list(it.product(*((self._add_key_2_every_val(para_name, self.test_parameter_dict[para_name]) for para_name in all_parameter_names))))
        testing_list = [ (list(para)+[instance]) for para in parameter_combination_list for instance in self.test_instance_list]
        
        # print(testing_list)
        result_list = []

        if(self.warmup_seconds > 0):
            print("Staring warmup for {} seconds".format(self.warmup_seconds))
            self._run_single_command('stress --cpu 1 --timeout ' + str(self.warmup_seconds))
            print("Finished warmup. Now starting the benchmark.")

        for i in range(self.repeat_time):
            for test in tqdm(testing_list):
                cmd = self.exec_path + " ".join(test)
                log_file_name = self.log_dir + " ".join(test).replace(" ", "_").replace("-", "")+"_run_"+str(i)+".log"
                exists = os.path.isfile(log_file_name)

                if not exists:
                    # run a single benchmark
                    result = self._run_single_command(cmd)
                    # write the result to a log file
                    with open(log_file_name, "w") as log_file:
                        log_file.write(cmd)
                        log_file.write('\n')
                        log_file.write(result)
                    result_list.append(result)
            
        return result_list

    def _run_single_command(self, cmd_str):
        # function to execute a single command
        p = subprocess.Popen(cmd_str.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, err = p.communicate()
        return output.decode('utf-8')
    
    def run_test_parallel(self, log_dir=None, process_count=mp.cpu_count()):
        if process_count > mp.cpu_count():
            print('number of of process should be smaller than cpu_count.')
            process_count = mp.cpu_count()

        if log_dir==None:
            log_dir = self.log_dir
        all_parameter_names = sorted(self.test_parameter_dict)
        # all_parameter_names = self.test_parameter_dict
        parameter_combination_list = list(it.product(*((self._add_key_2_every_val(para_name, self.test_parameter_dict[para_name]) for para_name in all_parameter_names))))
        testing_list = [ (list(para)+[instance]) for para in parameter_combination_list for instance in self.test_instance_list]
        
        # print(testing_list)
        result_list = []

        if(self.warmup_seconds > 0):
            print("Staring warmup for {} seconds".format(self.warmup_seconds))
            self._run_single_command('stress --cpu 1 --timeout ' + str(self.warmup_seconds))
            print("Finished warmup. Now starting the benchmark.")
  
        print("The first element in testing list is {}".format(testing_list[0]))

        
        with mp.Pool(process_count) as pool:
            result_list = pool.starmap_async(self._run_single_JSSP_instance, [(test, 0) for test in testing_list]).get()
            # for i in range(self.repeat_time):
            #     for test in tqdm(testing_list):
            #         pool.apply_async(self._run_single_JSSP_instance, args=(test, i))

        return result_list

    def _run_single_JSSP_instance(self, test, repeat_time):
        cmd = self.exec_path + " ".join(test)
        log_file_name = self.log_dir + " ".join(test).replace(" ", "_").replace("-", "")+"_run_"+str(repeat_time)+".log"
        exists = os.path.isfile(log_file_name)

        if not exists:
            # run a single benchmark
            result = self._run_single_command(cmd)
            # write the result to a log file
            with open(log_file_name, "w") as log_file:
                log_file.write(cmd)
                log_file.write('\n')
                log_file.write(result)
            return result

    # def add_testing_instances(self, instance_list):
    #     print("Start add_testing_instances")
    #     for instance in instance_list:
    #         if instance.split()[-1] in self.available_instance_list:
    #             self.test_instance_list.append(instance)
 
    def add_testing_instances(self, instance_list):
        print("Start add_testing_instances")
        for instance in instance_list:
            self.test_instance_list.append(instance)

    def _add_key_2_every_val(self, key, val_list):
        return [(key + " " + v) for v in val_list]
        
    def add_parameter_options(self, para_dict):
        # add values for benchmarks for one parameter
        assert len(para_dict) == 1, 'Please add one parameter at a time'
        key = list(para_dict.keys())[0]
        assert key in self.available_parameter_dict, 'Parameter {} is not avaiable'.format(key)
        val = para_dict[key]
        self.test_parameter_dict[key] = val
    
    def get_current_test_instances(self):
        return self.test_instance_list
    
    def get_current_test_parameters(self):
        return self.test_parameter_dict
    
    def get_available_instance_list(self):
        return self.available_instance_list
    
    def _get_avaialbe_benchmark_options(self, exec_path=None, help_cmd=' --help'):
        # get available parameter options from the program
        if exec_path==None:
            exec_path = self.exec_path
            
        help_str = self._run_single_command(exec_path + help_cmd)
        help_list = help_str.replace('\t', ' ').replace('\n', ' ').split(' ')

        # get parameter options
        parameter_list = [x for x in help_list if x.startswith('-') and len(x) >1][3:]
        parameter_dict = {}
        for option in parameter_list:
            parameter_dict[option] = []

        # get jssp instance options
        instance_list = "".join(help_list[help_list.index('instances:')+1:]).split(',')[:-1]
        
        return parameter_dict, instance_list