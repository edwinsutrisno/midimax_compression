# -*- coding: utf-8 -*-
"""
Demo for Midimax time-series data compression.

@author: ESutrisno
"""

import time
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import DatetimeTickFormatter, ColumnDataSource
from midimax_compression import compress_series

# Create a time-series of sine wave
n = 100000  # points
timesteps = pd.to_timedelta(np.arange(n), unit='s')
timestamps = pd.to_datetime("2022-04-18 08:00:00") + timesteps

sine_waves = np.sin(2 * np.pi * 0.02 * np.arange(n))
noise = np.random.normal(0, 0.1, n)
signal = sine_waves + noise
ts_data = pd.Series(signal, index=timestamps).astype('float32')

# Run compression
timer_start = time.time()
ts_data_compressed = compress_series(ts_data, 2)
timer_sec = round(time.time() - timer_start, 2)
print('Compression took', timer_sec, 'seconds.')


def format_fig_axis(fig):
    """Formatting the date stamps on the plot axis"""
    fig.xaxis.formatter = DatetimeTickFormatter(days=["%m/%d %H:%M:%S"],
                                                months=["%m/%d %H:%M:%S"],
                                                hours=["%m/%d %H:%M:%S"],
                                                minutes=["%m/%d %H:%M:%S"])
    fig.xaxis.axis_label = 'Timestamp'
    fig.yaxis.axis_label = 'Series Value'
    return fig


# Plot before
fig1 = figure(sizing_mode='stretch_both', tools='box_zoom,pan,reset')
line_before = fig1.line(x=ts_data.index, y=ts_data.values, line_width=2)
fig1 = format_fig_axis(fig1)
output_file(r'demo_output_before_compression.html')
save(fig1)

# Plot after
fig2 = figure(sizing_mode='stretch_both', tools='box_zoom,pan,reset')
line_after = fig2.line(x=ts_data_compressed.index, y=ts_data_compressed.values, line_color='green')
fig2 = format_fig_axis(fig2)
output_file(r'demo_output_after_compression.html')
save(fig2)

# Plot before and after together
fig3 = figure(sizing_mode='stretch_both', tools='box_zoom,pan,reset')
fig3.line(x=ts_data.index, y=ts_data.values, line_width=2)
fig3.line(x=ts_data_compressed.index, y=ts_data_compressed.values, line_color='green', line_dash='dashed')
fig3.scatter(x=ts_data_compressed.index, y=ts_data_compressed.values, marker='circle', size=8, color='green')
output_file('demo_output_before_and_after_compression.html')
save(fig3)
