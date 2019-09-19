from my_bias_corection_lib import BiasCorrection
from find_grid import find_station_grid
import numpy as np
import pandas as pd
import scipy
import seaborn as sns
import matplotlib.pyplot as plt

FIGSIZE = (8, 5)
DPI = 150

sns.set_style("whitegrid")
colors_palette = sns.color_palette("muted")
sns.set_palette(colors_palette)
sns.set_context(
    "paper",
    font_scale=1.15,
    rc={"lines.linewidth": 1.25, "lines.markersize": 7.5, "markers.linewidth": 0.25},
)
colors = sns.color_palette("muted")

# import data and cleansing data

obs = pd.read_csv("./observed/CHIANG_RAI_TH_TH000048303_1951-2019.csv")
mod_hist = pd.read_csv("./RCM/RCM_hist_TH.csv")

obs_lon, obs_lat = np.array(obs["LONGITUDE"])[0], np.array(obs["LATITUDE"])[0]

grid_lon, grid_lat = find_station_grid(
    obs_lat, obs_lon, np.array(mod_hist["lat"]), np.array(mod_hist["lon"])
)

print(f"nearest model grid: lat={grid_lat} lon={grid_lon}")

# select only one grid
mod_hist = mod_hist[(mod_hist["lon"] == grid_lon) & (mod_hist["lat"] == grid_lat)]

# change model unit to same unit as observed dataframe
mod_hist[["tas", "tasmin", "tasmax"]] -= 273.15
mod_hist["pr"] *= 86400

obs_ind = "PRCP"
mod_ind = "pr"

# convert date column to datetime type
obs["DATE"] = pd.to_datetime(obs["DATE"])
mod_hist["date"] = pd.to_datetime(mod_hist["date"])

# drop nan row in observed data frame
obs = obs.dropna()

# setting training and testing date interval
train_date = ["1970-01-01", "1999-12-31"]
test_date = ["2000-01-01", "2005-12-31"]

# split data to train and test
train_obs = obs[(obs["DATE"] >= train_date[0]) & (obs["DATE"] <= train_date[1])]
test_obs = obs[(obs["DATE"] >= test_date[0]) & (obs["DATE"] <= test_date[1])]

# select available observed date in model
train_mod = mod_hist[mod_hist["date"].isin(train_obs["DATE"])]
test_mod = mod_hist[mod_hist["date"].isin(test_obs["DATE"])]

# EDA
fig = plt.figure(figsize=(8, 5), dpi=120)
sns.distplot(train_obs[obs_ind], label="observed")
sns.distplot(train_mod[mod_ind], label="RCM model")
plt.title("training sample histogram plot")
plt.legend()
plt.xlabel("temperature")
plt.savefig("./bias_correction_present/training sample histogram plot.jpg", dpi=200)

num_quartile = 50
qth = np.linspace(0, 100, num_quartile + 1)

mod_per, obs_per = (
    np.percentile(train_mod[mod_ind], qth),
    np.percentile(train_obs[obs_ind], qth),
)

fig = plt.figure(figsize=(8, 8), dpi=120)
sns.scatterplot(mod_per, obs_per, label="RCM model-observed")
sns.scatterplot(obs_per, obs_per, label="observed-observed")
xx = np.arange(np.min([mod_per, obs_per]), np.max([mod_per, obs_per]))
sns.lineplot(xx, xx, label="y = x", color="k", alpha=0.5)
plt.xlabel("RCM model")
plt.ylabel("observed")
plt.title("Q-Q plot")
plt.savefig("./bias_correction_present/qqplot.jpg", dpi=200)

# Bias Correction
bc = BiasCorrection(train_obs[obs_ind], train_mod[mod_ind])

c = bc.constant_diff()
k = bc.coef_ratio()
a, b = bc.linear_regression()

fig = plt.figure(figsize=(8, 5), dpi=120)
sns.distplot(train_obs[obs_ind], label="observed")
sns.distplot(train_mod[mod_ind], label="RCM model")
sns.distplot(train_mod[mod_ind] - c, label=f"RCM model shifted {round(-c, 2)}")
plt.legend()
plt.title("bias correction $X_{corrected}$ = $X_{model}$ - c")
plt.xlabel("temperature")
plt.savefig("./bias_correction_present/bias correction const shifted.jpg", dpi=200)

fig = plt.figure(figsize=(8, 5), dpi=120)
sns.distplot(train_obs[obs_ind], label="observed")
sns.distplot(train_mod[mod_ind], label="RCM model")
sns.distplot(train_mod[mod_ind] * k, label=f"RCM model scaled {round(k, 2)}")
plt.legend()
plt.title("bias correction $X_{corrected}$ = $X_{model}$ * k")
plt.xlabel("temperature")
plt.savefig("./bias_correction_present/bias correction const scale.jpg", dpi=200)

fig = plt.figure(figsize=(8, 5), dpi=120)
sns.distplot(train_obs[obs_ind], label="observed")
sns.distplot(train_mod[mod_ind], label="RCM model")
sns.distplot(
    train_mod[mod_ind] * a + b,
    label=f"RCM model bias corrected a={round(a, 2)}, b={round(b, 2)}",
)
plt.legend()
plt.title("bias correction $X_{corrected}$ = $X_{model}$ * a + b")
plt.xlabel("temperature")
plt.savefig("./bias_correction_present/bias correction linear regression.jpg", dpi=200)

x_corrected_1 = np.percentile(train_mod[mod_ind] - c, qth)
x_corrected_2 = np.percentile(train_mod[mod_ind] * k, qth)
x_corrected_3 = np.percentile(train_mod[mod_ind] * a + b, qth)
mod_per, obs_per = (
    np.percentile(train_mod[mod_ind], qth),
    np.percentile(train_obs[obs_ind], qth),
)
xx = np.arange(np.min([mod_per, obs_per]), np.max([mod_per, obs_per]))

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8, 5), dpi=150)
bias_correction_qq = [x_corrected_1, x_corrected_2, x_corrected_3]

titles = ['RCM - c', 'RCM * k', 'RCM * a + b']

for i in range(len(bias_correction_qq)):
    sns.scatterplot(mod_per, obs_per, ax=axs[i], s=20)
    sns.scatterplot(
        bias_correction_qq[i], obs_per, ax=axs[i], s=25, label="bias corrected"
    )
    sns.lineplot(xx, xx, color="k", alpha=0.4, ax=axs[i])
    axs[i].set_xlabel("model")
    axs[i].set_ylabel("observed")
    axs[i].set_title(titles[i], fontsize=9)

plt.suptitle("Q-Q plot train sample", fontsize=12)
plt.savefig("./bias_correction_present/qq plot train sample.jpg", dpi=200)

x_corrected_1 = np.percentile(test_mod[mod_ind] - c, qth)
x_corrected_2 = np.percentile(test_mod[mod_ind] * k, qth)
x_corrected_3 = np.percentile(test_mod[mod_ind] * a + b, qth)
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8, 5), dpi=150)

obs_per = np.percentile(test_obs[obs_ind], qth)
mod_per = np.percentile(test_mod[mod_ind], qth)
xx = np.arange(np.min([mod_per, obs_per]), np.max([mod_per, obs_per]))
bias_correction_qq = [x_corrected_1, x_corrected_2, x_corrected_3]

titles = ['RCM - c', 'RCM * k', 'RCM * a + b']

for i in range(len(bias_correction_qq)):
    sns.scatterplot(mod_per, obs_per, ax=axs[i], s=20)
    sns.scatterplot(
        bias_correction_qq[i], obs_per, ax=axs[i], s=25, label="bias corrected"
    )
    sns.lineplot(xx, xx, color="k", alpha=0.4, ax=axs[i])
    axs[i].set_xlabel("model")
    axs[i].set_ylabel("observed")
    axs[i].set_title(titles[i], fontsize=9)

plt.suptitle("Q-Q plot test sample", fontsize=12)
plt.savefig("./bias_correction_present/qq plot test sample.jpg", dpi=200)


def mae(a, b):
    return np.mean(np.abs(a - b))


train_err = mae(np.array(train_obs[obs_ind]), np.array(train_mod[mod_ind]))
test_err = mae(np.array(test_obs[obs_ind]), np.array(test_mod[mod_ind]))

train_bc1 = mae(np.array(train_obs[obs_ind]), np.array(train_mod[mod_ind] - c))
train_bc2 = mae(np.array(train_obs[obs_ind]), np.array(train_mod[mod_ind] * k))
train_bc3 = mae(np.array(train_obs[obs_ind]), np.array(train_mod[mod_ind] * a + b))

test_bc1 = mae(np.array(test_obs[obs_ind]), np.array(test_mod[mod_ind] - c))
test_bc2 = mae(np.array(test_obs[obs_ind]), np.array(test_mod[mod_ind] * k))
test_bc3 = mae(np.array(test_obs[obs_ind]), np.array(test_mod[mod_ind] * a + b))

x = [
    "None",
    "RCM - c",
    "RCM * k",
    "RCM * a + b",
    "None",
    "RCM - c",
    "RCM * k",
    "RCM * a + b",
]
y = [train_err, train_bc1, train_bc2, train_bc3, test_err, test_bc1, test_bc2, test_bc3]

fig, axs = plt.subplots(2, 1, figsize=(8, 5), dpi=120, sharex=True)
axs[0].set_title("train sample MAE")
sns.barplot(y[:4], x[:4], ax=axs[0], orient="h")
axs[1].set_title("test sample MAE")
sns.barplot(y[4:], x[4:], ax=axs[1], orient="h")


axs[1].set_xticks(ticks=np.arange(0, np.max(y) * 1.1, 0.5))

plt.savefig("./bias_correction_present/MAE plot.jpg", dpi=200)


def rmse(a, b):
    return np.sqrt(np.mean((a - b) ** 2))


rmse_train_err = rmse(np.array(train_obs[obs_ind]), np.array(train_mod[mod_ind]))
rmse_test_err = rmse(np.array(test_obs[obs_ind]), np.array(test_mod[mod_ind]))

rmse_train_bc1 = rmse(np.array(train_obs[obs_ind]), np.array(train_mod[mod_ind] - c))
rmse_train_bc2 = rmse(np.array(train_obs[obs_ind]), np.array(train_mod[mod_ind] * k))
rmse_train_bc3 = rmse(
    np.array(train_obs[obs_ind]), np.array(train_mod[mod_ind] * a + b)
)

rmse_test_bc1 = rmse(np.array(test_obs[obs_ind]), np.array(test_mod[mod_ind] - c))
rmse_test_bc2 = rmse(np.array(test_obs[obs_ind]), np.array(test_mod[mod_ind] * k))
rmse_test_bc3 = rmse(np.array(test_obs[obs_ind]), np.array(test_mod[mod_ind] * a + b))

x = [
    "None",
    "RCM - c",
    "RCM * k",
    "RCM * a + b",
    "None",
    "RCM - c",
    "RCM * k",
    "RCM * a + b",
]
y = [
    rmse_train_err,
    rmse_train_bc1,
    rmse_train_bc2,
    rmse_train_bc3,
    rmse_test_err,
    rmse_test_bc1,
    rmse_test_bc2,
    rmse_test_bc3,
]

fig, axs = plt.subplots(2, 1, figsize=(8, 5), dpi=120, sharex=True)
axs[0].set_title("train sample RMSE")
sns.barplot(y[:4], x[:4], ax=axs[0], orient="h")
axs[1].set_title("test sample RMSE")
sns.barplot(y[4:], x[4:], ax=axs[1], orient="h")


axs[1].set_xticks(ticks=np.arange(0, np.max(y) * 1.1, 1))

plt.savefig("./bias_correction_present/RMSE plot.jpg", dpi=200)

# plt.show()