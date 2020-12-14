from nltk.tokenize import WordPunctTokenizer
import numpy as np

class JsspInstance:
    def __init__(self, name, size, raw_instance_list):
        self.name = name
        self._size = size
        self._raw_instance_list = raw_instance_list
        self.instance_array = self.parse_raw_list_2_numpy_array()
        self.num_of_jobs = size[0]
        self.num_of_machines = size[1]
        self._job_operation_time = dict({(ind, val) for ind, val in enumerate(np.sum(self.instance_array, axis=1)[:, 1])})
        self.max_operation_time = max(self._job_operation_time.values())
        
        self._machine_operation_mat = self._get_machine_operation_mat()
        self.machine_load = dict({(ind, val) for ind, val in enumerate(np.sum(self._machine_operation_mat, axis=1)[:,1])})
        self.max_machine_load = max(self.machine_load.values())
        
    
    def parse_raw_list_2_numpy_array(self, instance_list=None, size=None):
        # set default parameters
        if instance_list == None:
            instance_list=self._raw_instance_list
        if size == None:
            size = self._size
        # convert to numpy array
        instance_array = np.array(instance_list)
        machine_number = instance_array[0::2].reshape(size)
        duration = instance_array[1::2].reshape(size)
        return np.stack((machine_number, duration), axis=-1)
    
    def _get_machine_operation_mat(self, arr=None, size=None):
        if arr == None:
            arr = self.instance_array
        if size ==  None:
            size = self._size
            
        flat_arr = np.sort(arr.reshape((-1,2)))
        return flat_arr[flat_arr[:, 0].argsort()].reshape((self._size[1], self._size[0], 2))


def get_instance_dict(cpp_file):
	jssp_instance_list = []
	with open(cpp_file, 'r') as job_shop:
	    # file type check
	    assert cpp_file.rsplit('.')[-1] == 'hpp', 'can only work with hpp files'
	    
	    # read the whole file as a single stream
	    file_str = job_shop.read()
	    
	    # the following parsing looks a bit bruttle 
	    #    and may change based on the structure of the cpp file
	    jssp_list = file_str.split("namespace")[-1].split('const int*')[0].split('const int ')[1:]
	    
	    for item in jssp_list:
	        name = item.split('[]')[0]
	        s = item.split('[]')[1].split('{')[1].split('}')[0]
	        one_instance  = [int(char) for char in WordPunctTokenizer().tokenize(s) if char.isnumeric()]
	        assert 2*one_instance[0]*one_instance[1] == len(one_instance)-2
	        jssp_instance_list.append(JsspInstance(name, (one_instance[0], one_instance[1]), one_instance[2:]))



	jssp_instance_dict = {}
	for item in jssp_instance_list:
	    temp_dict = {}
	    temp_dict['instance_array'] = item.instance_array
	    temp_dict['num_of_jobs'] = item.num_of_jobs
	    temp_dict['num_of_machines'] = item.num_of_machines
	    temp_dict['max_operation_time'] = item.max_operation_time    
	    temp_dict['machine_load'] = item.machine_load    
	    temp_dict['max_machine_load'] = item.max_machine_load
	    jssp_instance_dict[item.name] = temp_dict


	print("Finish parsing {} jssp instances.".format(len(jssp_instance_dict)))
	return jssp_instance_dict