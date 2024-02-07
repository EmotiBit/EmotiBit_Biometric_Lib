# LSL Stream Viewer Installation Instructions
These instructions are for installing and using the [LSL Stream Viewer](https://github.com/intheon/stream_viewer).
Getting the install dependencies right was a bit tricky, so the exact steps used are included here:
- Install `Anaconda`
- Open `Anaconda Prompt` as admin
- Run the following commands in the `Anaconda Prompt`:
```
conda create --clone base -n LSL-Stream-Viewer
conda activate LSL-Stream-Viewer
conda update --all
conda update -n LSL-Stream-Viewer -c defaults conda
conda install --force-reinstall pyqt
conda install --force-reinstall qt
pip install git+https://github.com/intheon/stream_viewer.git
pip install stream_viewer
pip install pandas==1.5.3
```

# Running the LSL Stream Viewer
- Open `EmotiBit Oscilloscope`
- Connect to an EmotiBit and verify data is streaming
- Dropdown the `Output List` at the top right of the window
- Select `LSL`
- Open `Anaconda Prompt` as admin and run:
```
python -m stream_viewer.applications.main -s "[PATH_TO_INI_FILE]lsl_viewer_PPG.ini"
```
