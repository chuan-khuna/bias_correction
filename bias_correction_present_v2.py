from my_bias_corection_lib import BiasCorrection
import numpy as np
import pandas as pd
import scipy
import seaborn as sns
import matplotlib.pyplot as plt
color_palette = sns.color_palette("muted")
sns.set_palette(color_palette)
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.10, rc={"lines.linewidth": 1.5, "lines.markersize": 5})

import find_grid

mod_ind = "tas"
obs_ind = "TAVG"
grid_step = 1.875

mod = pd.read_csv("./RCM/RCM_hist_TH.csv")
obs = pd.read_csv(f"./observed_clean/{obs_ind}.csv")
stations = pd.read_csv("./observed_clean/stations.csv")

# chiang mai/chiang rai station
mod_lon=99.375
mod_lat=19.585

obs['DATE'] = pd.to_datetime(obs['DATE'])
mod['date'] = pd.to_datetime(mod['date'])
mod = mod[(np.round(mod['lat'], 3) == mod_lat) & (mod['lon'] == mod_lon)]
mod[['tas', 'tasmin', 'tasmax']] -= 273.15
mod['pr'] *= 86400

selected_station = find_grid.filter_station(mod_lat, mod_lon, stations)
print(selected_station)
station_id = np.array(selected_station['STATION'])[0]

obs_data = obs[['DATE', station_id]].dropna()
obs_data = obs_data.rename(columns={station_id: obs_ind})

train_date = ["1970-01-01", "1999-12-31"]
test_date = ["2000-01-01", "2005-12-31"]
train_obs = obs_data[(obs_data['DATE'] >= train_date[0]) & (obs_data['DATE'] <= train_date[1])]
train_mod = mod[mod['date'].isin(train_obs['DATE'])]
test_obs = obs_data[(obs_data['DATE'] >= test_date[0]) & (obs_data['DATE'] <= test_date[1])]
test_mod = mod[mod['date'].isin(test_obs['DATE'])]

bc = BiasCorrection(train_obs[obs_ind], train_mod[mod_ind]) 
c = bc.constant_diff()
k = bc.coef_ratio()
a, b = bc.linear_regression()

fig = plt.figure(figsize=(8, 5), dpi=150)
sns.scatterplot(train_obs['DATE'], train_obs[obs_ind], linewidth=0.25, label="observed")
sns.scatterplot(train_mod['date'], train_mod[mod_ind], linewidth=0.25, alpha=0.5, label="RCM", s=10)
sns.scatterplot(train_mod['date'], train_mod[mod_ind] - c, linewidth=0.25, alpha=0.75, label="bias corrected", s=10)
plt.show()