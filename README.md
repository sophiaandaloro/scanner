# Scanning through configuration settings in strax
## Overview
When we work in strax, we often need to look at editing configuration settings that change how we process strax data.
These include things like:
- s2_min_pmts (how many pmts have to be hit to count a peak as an s2?)
- save_outside_hits (data reduction: we only save data around a certain margin of the hits.)
- nn_architecture (really important for position reconstruction)
- tail_veto_threshold (at what size of peaks do we start to turn on the software high energy veto?)
This is one of the settings that Sophia is studying with this code.

To see the full list, check out the straxen documentation. There's a LOT you can change, dozens of settings and parameters which can affect each level of the data we save.

## Goals and Processing
### Goals: 
With this type of code, the goal is that you can “scan” over all parameters, or strax configuration settings, pertinent to your particular analysis, to get the best settings which correspond to excellent data processing goals, whatever that might look like for you.

For instance, if you were testing out a bunch of position reconstruction settings on kr-83m data, you'd want to pick the settings which show, among other things, the most uniform radial distribution throughout the detector.
There are hundreds of possible options for you to choose, though. So do you go about manually changing each possible combination of settings in a notebook, single-job format? That's not very effective! Instead, we have build a code which you can change to your specific study, which will submit individual jobs to dali which will process the data of your choosing.

### Processing: 
In short, you will set up the settings you want to take a look at. Then the code will submit a job for each unique combination of those settings to dali. Each job will process the data, returning all strax-processed data (with the configuration settings attached so you can retrieve them later) to a strax_data folder. Then, all you need to do is go into a notebook as normal and grab the data of your choice, specifying the settings you want to take a look at.

This makes the job of analyzing which strax settings to choose for XENONnT data-taking much more efficient, and in the long run the code's framework can be used as a “monitor” of sorts.

## Scanner Tutorial
The first thing you will want to do is ssh into Midway. You can do this as stated in the analysis guide.
Also as other places can help you figure out, ensure you have your favorite strax-enabled conda env activated.
Make or move into a directory where you want to do your processing and save your data within. You will also have the option to change where your newly processed data is saved but it will automatically save within the directory you run your script in.
Ensure you have the two python files from the repo linked above (mystuff.py and scanner.py) to your directory.
At this point, edit were indicated within mystuff.py to create the configuration settings you want to process for.
Each of the unique configurations possible from the lists you provide will be submitted as individual jobs to dali later.
After you do that, you should be able to run
`python mystuff.py `
on your terminal and it'll work out-of-the-box. However, you can change a lot so let's look at everything in scanner.py to discuss what the code is actually doing and what your options are.

So, running mystuff.py will call the scanner.py function: scan_parameters. Within that, you will be submitting a batch queue job for each of the parameter settings you had specified earlier.

This job should look very familiar to anyone who's looked under the hood of what a jupyter job submission actually looks like, because it's based on that code!
Here's the JOB_HEADER:
```
JOB_HEADER = """#!/bin/bash
#SBATCH --job-name=scan_{name}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={n_cpu}
#SBATCH --time={max_hours}:00:00
#SBATCH --partition={partition}
#SBATCH --account=pi-lgrandi
#SBATCH --qos={partition}
#SBATCH --output={log_fn}
#SBATCH --error={log_fn}
{extra_header}
# Conda
. "{conda_dir}/etc/profile.d/conda.sh"
{conda_dir}/bin/conda activate {env_name}
echo Starting scanner
python {python_file} {run_id} {data_path} {config_file} 
"""
```
So, within a job, we are able to configure those settings below. The defaults are: - partition: dali - env_name: strax - max_hours: 8 - n_cpu: 40 (speeds up the job, but increasing cpus can take your jobs way longer to get a node and start running) - name: magician (Supply your name so you can keep track of which jobs are yours easier.)

And changing those settings is done at the following point within the submit_setting function:
```
        f.write(JOB_HEADER.format(
            **job_config,
            log_fn=log_fn,
            python_file=os.path.abspath(__file__),
            config_file = config_fn,
            name=name,
            run_id=run_id,
            target=target,
            data_path=output_directory,
            xenon1t=xenon1t
        ))
```

### Strax Settings
You can change many things with this scanner. You can even specify your own plugins to use. We will show how those options can be done with the example given in the code on the repo.

Here are all of the options to change in mystuff.py.

- If trying out your own plugins, ensure you import the module(s). Then, you can specify the different plugins to be registered in a list format.
- If you don't want to make your own plugins, just set register=None in mystuff.py.
- target: specifies what data type you would like to get from processing.
- name: add your initials to keep track of who's running what on dali.
- output_directory: Default is ./strax_data, the directory where you will save your processed data. Make sure to purge this periodically if you are creating an extreme amount of new data.
- parameter_dict: Your strax configuration setting options will go here. Specify a list of run(s), and an arbitrary list of settings.

What happens is that strax will enumerate and run over all possible combinations for these settings.
So in this example:
```
 paramter_dict = {'run_id': ['007447'], # List of run_ids to apply scan to
                 'baseline_window': [(0,30), (0,40)], #An example of a tuple-style setting
                 'save_outside_hits_left': [20, 40], #An example of a single-valued setting
                }      
```
What are we creating? We are creating the following unique settings to submit each individually as a job:

- 'run_id': '007447', 'baseline_window': (0,30), 'save_outside_hits_left': 20
- 'run_id': '007447', 'baseline_window': (0,30), 'save_outside_hits_left': 40
- 'run_id': '007447', 'baseline_window': (0,40), 'save_outside_hits_left': 20
- 'run_id': '007447', 'baseline_window': (0,40), 'save_outside_hits_left': 40

### Specifying job submission settings:
At the end of mystuff.py, we specify some job settings. These include the following:
- n_cpu: How many cpus per setting combination to use for the job. Default is kept low.
- max_hours: 1 hour default. Jobs automatically end when they finish processing, or at this cutoff point.
- partition: 'xenon1t' chosen for now. Can also specify 'dali' and things work fine.
- xenon1t: Boolean. Set to False if working with nT data (the default), or set to True if using 1t data. This specifies the context used.

### What's going on under the hood, though?
We can turn to scanner.py to see what's actually happening.

When we call scan_parameters in mystuff.py, we specify a whole lot of settings in strax and for computing purposes.

We first ensure user has specified at least some run_id.
Then we turn our parameter dictionary into an iterated form, where we iterate all unique setting combinations, as we explored above.
We run a final check, _user_check to get final confirmation from the user that all of the iterated settings from the previous step look okay to them, before blindly submitting many jobs.
We add all of our job configurations, like number of cpus to request, to our job submission file. If not specified, we'll add the default settings there and/or raise an error that you forgot to specify settings.
After a few final checks, we run a loop, calling submit_setting for each unique setting combo.
submit_setting does the following:

Creates a log, configuration, and job files that specify all of the outputs you would otherwise see if you ran scanner.py directly.
The _conf file (short for configuration) will hold your setting number, as well as all of the unique settings you specified. This is how you trace where your code failed, if it does.
Use the _conf file to understand what settings triggered an error, which will be present in the _log file.
submit_setting then finally writes out a job header to submit to the batch queue. This job runs scanner.py directly, given the unique setting (remember we are in a for loop still!)

With the job submitted, and scanner.py called directly in the job submission, we turn to the final part of this process. We run work, which simply registers the straxen context you need (depending on the data you are using) and calls st.make(target) to make your target data in your target directory.
The job closes out, writing the time of the job to your _log file, if you care to see how long it's taking. This can be helpful for debugging.

## Version & Release Notes
### v0.2.0 (Current)
Features: 
1. Now functional with both XENONnT and XENON1T data, via argument specification.
2. You can now pass your own plugins as configuration options. Simply import your plugin(s) and append to a plugin list. 
3. Several quality of life changes. You can double-check your strax settings before submitting your jobs via a command-line prompt. Log files are now easily traceable, and include more information about your jobs. Better documentation = happier analysts!
