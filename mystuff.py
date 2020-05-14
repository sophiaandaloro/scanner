import scanner
import sys

import straxen
### EDIT BELOW TO CHANGE CONFIG SETTINGS ###
# In case you want to register any non-standard plugins which is not part of the offical straxen 
# you have to specify the path where the .py file with the plugin can be found:
# sys.path.append('/path/to/plugin')
# and import it.
# from HitFinderThresholdPlugin import MyPlugin

# TODO: Change these parameters back to some default example...
run_id = '007447' 
target = 'led_calibration'# 'hitfinder_hits'
name = 'hf' # TODO: I think Sophia mentioned a max number of characters. 
output_directory = './strax_data'
# Plugins to be registered, can be None, single Plugin or a list of Plugins.
register=None
paramter_dict = {'run_id': run_id, # can also be a list of run_ids, to apply our scan to multiple runs.
                 'threshold': 50,
                 'save_outside_hits_left': [10, 20],
                 'save_outside_hits_right': [100]}

#scan over everything in strax_options
scanner.scan_parameters(target,
                        paramter_dict,
                        register=register,
                        output_directory=output_directory,
                        name=f'{name}_scan',
                        job_config={'n_cpu': 10, 
                                    'max_hours': 1,
                                   'partition': 'xenon1t'},
                        xenon1t=False
                       )
