# Welcome to the EmotiBit Python Library

## Setup Python virtual environment
1) `cd` into the `py` directory under the root directory
1) Run `python -m venv emotibit-env` to create a virtual environment named `emotibit-env`
1) Activate the virtual environment by running
    * Windows: `.\venv\Scripts\activate`
    * macOS/Linux: `source emotibit-env/bin/activate`
1) The terminal should now start with `(emotibit-env)` followed by path to current working directory (ex. `(emotibit-env) C:\Users\username\Documents\...`)
1) Install required packages by running `pip install -r requirements.txt`
1) Install the `emotibit` package by running `pip install -e .` while in the `py` directory

## Checkout the [examples](./examples) folder to start working with the recorded data.
**Note:** Before running any example, make sure that `emotibit-env` has been activated so that the `emotibit` package and other dependencies can be found

### Python Data Viewer
The Python Data viewer is an interactive tool designed to visualize the data stored on the SD-Card from the EmotiBit.
- Refer to `py/emotibit/examples/dataviewer_example/README.md` for detailed instructions on how to use Data Viewer

