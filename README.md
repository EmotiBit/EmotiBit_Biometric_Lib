# Emotibit_Biometric_Lib
Biometric library for processing EmotiBit data
## Data Analyser
 - added on September 6 2019
The Data Analyzer is tool which can be used for visualizing the data stored on the SD-Card. It can produce a simultaneous view of 18 channel sensor data, which can be viewed interactively. The timeline indicator at the bottom is useful for checking the segment of data currently on the plots.
### The python visualizer has the folowing functions available for use
- You can **zoom** into any part of the plot using the default `zoom button` provided in the spyder. Just press the magnifying glass icon, click and drag anywhere on the plot to zoom in on that portion.
- The `move button` is located next to the `zoom button`. you can press this button and _click and drag_ on any plot to slide through the data. If you press the `x` button or the `y` button simultaneously when moving, the data is moves only in the _x or the y direction_, respectively. 
- You can press the home button to go back to the original view of the data.
- **Keyboard Shortcuts**
  - **_hide/show DC markers_**: The Cutoffs(instances when the sensor data goes out of bounds) in the data, are marked with red verticle lines. You can toggle the visibility of the DC markers in any individual plot by clicking on the plot and presing the `space` key. Pressing it once remoes the DC markers from that plot. Pressing it again will re-mark the lines on the plot.
  - **_Y-Axis Autoscale_**: After you zoom into any portion of the data, the data on each plot can be scaled . by pressing the `a` key. This adjusts the Y-Axis limits for each plot.
  - **_Mark any point in time on the fly_**: Click on the point(any location within the plot) you want to highlihgt, and press `m`. This will highlight a region around that point in time on all plots. This is great way to see the relative position on any activity across plots. Click anywhere on the figure, outside the plots to remove this highlight
