# Welcome to the EmotiBit Python Library

## Setup Anaconda and Spyder
* Setup Anaconda Python
  * See these helpful instructions - https://medium.com/@Shreedharvellay/anaconda-jupyter-spyder-things-you-need-to-know-3c808d824739
    * Briefly:
      * Install Anaconda - https://www.anaconda.com/download/
* Download or clone EmotiBit_Biometric_Lib to your computer
* Open Anaconda Navigator
* Import EmotiBit_Biometric_Lib/py/EmotiBit-pyenv.yml into Anaconda Navigator Environments
  * <img src="https://github.com/EmotiBit/EmotiBit_Biometric_Lib/assets/537062/5ff71b46-17c7-4fd8-87eb-0e92b0cedd2f" width="300">
* Use `conda develop py` while in EmotiBit_Biometric_Lib to add the py directory to path

## Checkout the [examples](./examples) folder to start working with the recorded data.
For example, to run `scorer_example.py`:
1) Setup the Anaconda environment as [previously mentioned](#setup-anaconda-and-spyder)
2) Open up Anaconda terminal (Command Prompt or Powershell)
3) Activate the environment by running `conda activate EmotiBit-pyenv`
4) `cd` to `examples/scorer_example`
5) Unzip SampleDataForHRScorer.zip into the folder
6) Run `python scorer_example.py`
7) After the program has finished running, the terminal should show some statistics and there should be a new image in the directory with a plot of the two data files

## Python Data Viewer
The Python Data viewer is an interactive tool designed to visualize the data stored on the SD-Card from the EmotiBit.
- Run the [`dataviewer_example.py`](./examples/dataviewer_example) example under the `py/Examples/dataviewer_example` folder the same as above.
  - Make sure to update the `file_dir` and `file_base` variables to point to your data file.

