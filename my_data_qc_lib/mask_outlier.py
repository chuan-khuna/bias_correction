import pandas as pd
import numpy as np

def mask_outlier_by_std(dataframe, col):
    """
        mask outlier of selected column in dataframe

        dataframe: dropped nan dataframe
    """

    mean = np.round(dataframe[col].mean(), 3)
    std = np.round(dataframe[col].std(), 3)
    outlier = dataframe[abs(dataframe[col] - mean) > 3*std]

    return outlier