	�3���@�3���@!�3���@	�>H�a�?�>H�a�?!�>H�a�?"e
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails$�3���@ �o_��?Aj�t��@Y�D���J�?*	     �_@2f
/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap������?!�H$�DB@)�ܵ�|У?1����x>@:Preprocessing2U
Iterator::Model::ParallelMapV2�p=
ף�?!�r�\.�9@)�p=
ף�?1�r�\.�9@:Preprocessing2l
5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat� �	��?!�@8@)�{�Pk�?1
�B�P4@:Preprocessing2F
Iterator::Model�,C��?!&��d2�A@)�HP��?1�f��l6#@:Preprocessing2v
?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::TensorSlice� �	�?!�@@)� �	�?1�@@:Preprocessing2Z
#Iterator::Model::ParallelMapV2::Zip��u���?!m6��f3P@)��ZӼ�t?1�@ @:Preprocessing2x
AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor{�G�zt?!�����~@){�G�zt?1�����~@:Preprocessing:�
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
�Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
�Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
�Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
�Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)�
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis�
both�Your program is POTENTIALLY input-bound because 3.4% of the total step time sampled is spent on 'All Others' time (which could be due to I/O or Python execution or both).no*no9�>H�a�?>Look at Section 3 for the breakdown of input time on the host.B�
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown�
	 �o_��? �o_��?! �o_��?      ��!       "      ��!       *      ��!       2	j�t��@j�t��@!j�t��@:      ��!       B      ��!       J	�D���J�?�D���J�?!�D���J�?R      ��!       Z	�D���J�?�D���J�?!�D���J�?JCPU_ONLYY�>H�a�?b 