# Machine Learning
This is the repository for the TUM Phoenix Autonomous Drive Machine Learning applications. 
* [Literature (TUM Phoenix Wiki)](https://wiki.tum.de/display/phoenix/Machine+Learning)
* [Todo List (Issues page)](https://github.com/tum-phoenix/drive_ml/issues)

## Use on TUM Phoenix Hardware
There is a workstation available with all software preinstalled and decent training hardware (Nvidia GTX1070 8GB). Just ask the project leader for an account. Access only from TUM University network (or use LRZ-VPN).

## Use on own Hardware
If you want to install it on your own device follow these instructions:
1. Install [requirements](https://github.com/tum-phoenix/drive_ml/blob/master/requirements.txt) using pip3 (`sudo pip3 install -r requirements.txt`)
2. login with your username and generate config `jupyter notebook --generate-config`
3. add following [File Save Hook](http://jupyter-notebook.readthedocs.io/en/stable/extending/savehooks.html) to your config `~/.jupyter/jupyter_notebook_config.py`:
```
def scrub_output_pre_save(model, **kwargs):
    """scrub output before saving notebooks"""

    # only run on nbformat v4
    if model['nbformat'] != 4:
        return

    for cell in model['cells']:
        if cell['cell_type'] != 'code':
            continue
        cell['outputs'] = []
        cell['execution_count'] = None

c.FileContentsManager.pre_save_hook = scrub_output_pre_save
```
4. Start Jupyter notebook and start editing files

## Datasets
We mainly use GTSRB Dataset. It will be loaded automatically when running the Jupyter notebooks. Additional files are on the TUM Phoenix server (please contact project leader). You may need to change the paths to your environment. Please make sure they have the same structure of [GTSRB structure](http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset#Structure).

## Structure of sign recognition folder
- `logs` (tensorboard log files)
- `models` (trained and untrained netmodels)
- `dicts` (translation: signs <-> category number)
- `utilities` (utility functions and scripts for data processing, training helpers, ...)
