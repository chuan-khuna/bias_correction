import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
sns.set_palette(sns.color_palette("muted"))
sns.set_context("paper", font_scale=1.0, rc={"lines.linewidth": 1.0})

DPI = 200
FIGSIZE = (8, 5)
COLOR_MAP = "Spectral_r"


def plot_missing_heatmap(dataframe, title, directory):
    """
        dataframe: dataframe that index is date
            monthly dataframe [yyyy-mm, yyyy-mm] or group by month dataframe [1, 2, ...12]
        title: figure title, and image output filename
        directory: image file output folder
    """

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    plt.title(title)
    try:
        dataframe.index = dataframe.index.strftime("%Y-%m")
        sns.heatmap(dataframe, cmap=COLOR_MAP)
    except:
        # if month dataframe
        sns.heatmap(dataframe, cmap=COLOR_MAP, square=True)
        plt.tight_layout()
    fig.savefig(f"./{directory}/{title}.jpg", dpi=DPI)
