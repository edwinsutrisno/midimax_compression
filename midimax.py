# -*- coding: utf-8 -*-
"""
Midimax Data Compression for Time-Series

Author: Edwin Sutrisno
Changes:
    April 16, 2022: First version (Edwin Sutrisno).
"""

import pandas as pd


def compress_series(inputser: pd.Series, compfactor=2):
    """
    Split into segments and pick 3 points from each segment, the minimum,
    median, and maximum. Segment length = int(compfactor x 3). So, to achieve a
    compression factor of 2, a segment length of 6 is needed.

    Parameters
    ----------
    inputser : pd.Series
        Input data to be compressed.
    compfactor : float
        Compression factor. The default is 2.

    Returns
    -------
    pd.Series
        Compressed output series.

    """
    # If comp factor is too low, return original data
    if (compfactor < 1.4):
        return inputser

    win_size = int(3 * compfactor)  # window size

    # Create a column ofsegment numbers
    ser = inputser.rename('value')
    ser = ser.round(3)
    wdf = ser.to_frame()
    del ser
    start_idxs = wdf.index[range(0, len(wdf), win_size)]
    wdf['win_start'] = 0
    wdf.loc[start_idxs, 'win_start'] = 1
    wdf['win_num'] = wdf['win_start'].cumsum()
    wdf.drop(columns='win_start', inplace=True)
    del win_size, start_idxs

    # For each window, get the indices of min, median, and max
    def get_midimax_idxs(gdf):
        if len(gdf) == 1:
            return [gdf.index[0]]
        elif gdf['value'].iloc[0] == gdf['value'].iloc[-1]:
            return [gdf.index[0]]
        elif len(gdf) == 2:
            return [gdf.index[0], gdf.index[1]]
        else:
            return [gdf.index[0], gdf.index[len(gdf) // 2], gdf.index[-1]]

    wdf = wdf.dropna()
    wdf_sorted = wdf.sort_values(['win_num', 'value'])
    midimax_idxs = wdf_sorted.groupby('win_num').apply(get_midimax_idxs)

    # Convert into a list
    midimax_idxs = [idx for sublist in midimax_idxs for idx in sublist]
    midimax_idxs.sort()
    return inputser.loc[midimax_idxs]
