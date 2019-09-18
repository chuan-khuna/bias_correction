import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
sns.set_palette(sns.color_palette("muted"))
sns.set_context("paper", font_scale=1.0, rc={"lines.linewidth": 0.85, "lines.markersize": 5})

DPI = 200
FIGSIZE = (8, 5)
COLOR_MAP = "Spectral_r"


def plot_outlier(dataframe, col_list, x_col, outlier_dict, title, directory):
    """
        outlier_dict: outlier dataframe in dictionary type
        example:
        {
            "col0": df_col0,
            "col1": df_col1
        }
    """
    num_cols = len(col_list)
    fig, axs = plt.subplots(
        nrows=num_cols, ncols=1, figsize=FIGSIZE, dpi=DPI, sharex=True
    )
    for i in range(num_cols):
        sns.lineplot(x=x_col, y=col_list[i], data=dataframe, ax=axs[i])
        sns.scatterplot(
            x=x_col,
            y=col_list[i],
            data=outlier_dict[col_list[i]],
            color="red",
            s=50,
            ax=axs[i],
        )
    fig.suptitle(title, fontsize=14)
    fig.savefig(f"./{directory}/{title}.jpg", dpi=DPI)
