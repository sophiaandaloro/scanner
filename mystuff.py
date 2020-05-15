import scanner
import sys

import straxen
### EDIT BELOW TO CHANGE CONFIG SETTINGS ###
# In case you want to register any non-standard plugins which is not part of the offical straxen 
# you have to specify the path where the .py file with the plugin can be found:
sys.path.append('/home/dwenz/python_scripts/XENONnT/analysiscode/PMTs/HitFinder/Threshold')
# and import it.
from HitFinderThresholdPlugin import HitIntegratingAnalysis


# TODO: Change these parameters back to some default example...
target = 'hitfinder_hits'
name = 'hf' # TODO: I think Sophia mentioned a max number of characters. 
output_directory = './strax_data'
register=[HitIntegratingAnalysis] # Plugins to be registered, can be None, single Plugin or a list of Plugins.

paramter_dict = {'run_id': ['007447', '007455'], # can also be a list of run_ids, to apply our scan to multiple runs.
                 'threshold': 15,
                 'save_outside_hits_left': 20,
                 'save_outside_hits_right': [100, 120]}

#scan over everything in strax_options
scanner.scan_parameters(target,
                        paramter_dict,
                        register=register,
                        output_directory=output_directory,
                        name=f'{name}_scan',
                        job_config={'n_cpu': 2, 
                                    'max_hours': 1,
                                   'partition': 'xenon1t'},
                        xenon1t=False
                       )