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
target = 'hitfinder_area_per_record'
name = 'hf' # TODO: I think Sophia mentioned a max number of characters. 
output_directory = '/dali/lgrandi/wenz/strax_data/HitFinder/nT'
register=[HitIntegratingAnalysis] # Plugins to be registered, can be None, single Plugin or a list of Plugins.


# Here are some notes how you have to specifiy the parameter settings:
# 1.) The key word in the following dict must be equivalent to the key
#     word in the corresponding strax.Option of your plugin
# 2.) All values can be either single objects like int, float, string or a list.
#     In case you specifiy a list the scanner will check all possible parameter
#     combination for you. e.g. for {a: [1,2], b:[10, 20]} --> 1.: a=1, b=10, 2.: a=1, b=20, 3.: a=1, b=10, 4.: a=2, b=20
# 3.) tuple, (round brackets () ) have a special meaning for the scanner with tuples
#     we indicate settings which should not be terated e.g. if you have a setting
#     like "search_window": (110, 140) or e.g. a left and right hit extension. You can 
#     also iterate over tuple-settings when specified as a list. E.g. if you want to 
#     check multiple search windows you can do "search_window": [(110, 140), (128, 150), (134, 170)]
paramter_dict = {'run_id': '007447', # can also be a list of run_ids, to apply our scan to multiple runs.
                 'threshold': [8, 10, 15, 20, 25],
                 'save_outside_hits_left': [20, 30, 40],
                 'save_outside_hits_right': [140, 160, 180, 200, 220, 240, 260, 280]}

#scan over everything in strax_options
scanner.scan_parameters(target,
                        paramter_dict,
                        register=register,
                        output_directory=output_directory,
                        name=f'{name}_scan',
                        job_config={'n_cpu': 2, 
                                    'max_hours': 2,
                                   'partition': 'xenon1t'},
                        xenon1t=False
                       )
