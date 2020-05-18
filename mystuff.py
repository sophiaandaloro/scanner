import scanner
import sys

import straxen

### EDIT BELOW TO CHANGE CONFIG SETTINGS ###
# In case you want to register any non-standard plugins which is not part of the offical straxen 
# you have to specify the path where the .py file with the plugin can be found:
# sys.path.append('/path/to/plugin')
# and import it.
# from HitFinderThresholdPlugin import HitIntegratingAnalysis
from led_calibration import LEDCalibration
# Target to acquire with strax (should be a data kind)
target = 'led_calibration'# 'hitfinder_hits'
# Plugins to be registered, can be None, single Plugin or a list of Plugins.
register=[LEDCalibration]
# register=None
# Add your initials so your scanner jobs can be found/uniquely ID'd 
# (keep characters <5 to not get thrown to resources queue)
name = 'sja' 
output_directory = './strax_data' #where the new processed data will be saved.

# Here are some notes how you have to specifiy the parameter settings:
# 1.) The key word in the following dict must be equivalent to the key
#     word in the corresponding strax.Option of your plugin
# 2.) All values can be either single objects like int, float, string or a list.
#     In case you specifiy a list the scanner will check all possible parameter
#     combination for you. e.g. for {a: [1,2], b:[10, 20]} --> 1.: a=1, b=10, 2.: a=1, b=20, 3.: a=1, b=10, 4.: a=2, b=20
# 3.) tuple, (round brackets () ) have a special meaning for the scanner with tuples
#     we indicate settings which should not be terated e.g. if you have a setting
#     like "search_window":  and right hit e(110, 140) or e.g. a leftxtension. You can 
#     also iterate over tuple-settings when specified as a list. E.g. if you want to 
#     check multiple search windows yoseu can do "arch_window": [(110, 140), (128, 150), (134, 170)]
paramter_dict = {'run_id': ['007447'], # List of run_ids to apply scan to
                 'baseline_window': [(0,30), (0,40)], #An example of a tuple-style setting
                 'save_outside_hits_left': [20], #An example of a single-valued setting
                }

#scan over everything in strax_options
#Options here: 
# n_cpu: How many CPUs per each setting to request. Try to limit number
# max_hours: Job will automatically cancel if max is reached. 
#            Otherwise job will finish once the function scan_parameters is complete.
scanner.scan_parameters(target,
                        paramter_dict,
                        register=register,
                        output_directory=output_directory,
                        name=f'{name}_scan',
                        job_config={'n_cpu': 2, 
                                    'max_hours': 1,
                                   'partition': 'xenon1t'},
                        xenon1t=False #Specify True if working with 1t data 
                       )
