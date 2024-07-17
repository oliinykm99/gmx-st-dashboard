import numpy as np
import pandas as pd

def get_tvl(data, time_col, tvl_col):
    current_time = pd.Timestamp.now()
    closest_active_idx = (data[time_col] - current_time).abs().argmin()
    current_tvl = data.iloc[closest_active_idx][tvl_col]
    if closest_active_idx == 0:
        prev_active_idx = 1
    else:
        prev_active_idx = closest_active_idx - 1
    prev_tvl = data.iloc[prev_active_idx][tvl_col]
    delta_active_tvl = np.log(current_tvl / prev_tvl) * 100 if prev_tvl != 0 else 0
    return current_tvl, delta_active_tvl

def get_open_interest(data, time_col, open):
    current_time = pd.Timestamp.now()
    closest_active_idx = (data[time_col] - current_time).abs().argmin()
    current_open = data.iloc[closest_active_idx][open]
    if closest_active_idx == 0:
        prev_active_idx = 1
    else:
        prev_active_idx = closest_active_idx - 1
    prev_open = data.iloc[prev_active_idx][open]
    delta_open = np.log(current_open / prev_open) * 100 if prev_open != 0 else 0
    return current_open, delta_open

def get_cumulative_volume(data, time_col, vol_col):
    current_time = pd.Timestamp.now()
    closest_active_idx = (data[time_col] - current_time).abs().argmin()
    current_volume = data.iloc[closest_active_idx][vol_col]
    if closest_active_idx == 0:
        prev_active_idx = 1
    else:
        prev_active_idx = closest_active_idx - 1
    prev_volume = data.iloc[prev_active_idx][vol_col]
    delta_open = np.log(current_volume / prev_volume) * 100 if prev_volume != 0 else 0
    return current_volume, delta_open
