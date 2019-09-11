import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
sns.set_palette(sns.color_palette("muted"))
sns.set_context("paper", font_scale=1.0, rc={"lines.linewidth": 1.0})

DPI = 200
FIGSIZE = (8, 5)

def box_and_hist_plot(dataframe, columns_list, xlabel, title, directory):
    """
        dataframe: dropped nan dataframe
        columns_list: list of column headers as distribution plot label
        xlabel: custom graph x label (column type)
        title: figure title, and image output filename
        directory: image file output folder
    """
    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=FIGSIZE,
        dpi=DPI,
        gridspec_kw={"height_ratios": (0.25, 0.75)},
        sharex=True,
    )
    fig.suptitle(title, fontsize=14)
    for col_name in columns_list:
        sns.distplot(dataframe[col_name], ax=axs[1], label=col_name)
    sns.boxplot(data=dataframe[columns_list], ax=axs[0], orient='h')
    axs[1].legend()
    axs[1].set_xlabel(xlabel)
    fig.savefig(f"./{directory}/{title}_box_hist.jpg", dpi=DPI)
