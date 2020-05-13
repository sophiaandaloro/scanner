import sys 

import numpy as np
from collections import OrderedDict
import scanner

parameters = OrderedDict()

# IF YOU WANT TO REGISTER YOUR OWN PLUGIN FOR THE SCAN, USE THESE LINES. 
# In case you want to register any non-standard plugins which is not part of the offical straxen 
# you have to specify the path where the .py file with the plugin can be found:
sys.path.append('/path/to/your/plugin/')
# and import it.
import MyPlugin # Or whatever your plugin is named. Skip if not doing plugin.



target = ''
name = 'me' # A short (<5 characters?) name to find your scanner among the masses of jobs. Initials are good.
output_directory = './strax_data'
# Plugins to be registered, can be None, single Plugin or a list of Plugins.
register = HitCounting 

#Specify here all of the config settings you want to look at. 
paramter_dict = {'run_id': run_id, # can also be a list of run_ids. 
                 'threshold': 15,
                 'save_outside_hits_left': [10, 20, 30, 40],
                 'save_outside_hits_right': [100, 120, 140, 160, 180, 200, 220, 240, 260]}

#scan over everything in strax_options. scanner.py will enumerate over all that you've provided. 
scanner.scan_parameters(target,
                        paramter_dict,
                        register=register,
                        output_directory=output_directory,
                        name=f'{name}_scan',
                        job_config={'n_cpu': 2, 
                                    'max_hours': 1},
                        xenon1t=False
                       )
