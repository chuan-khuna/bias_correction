import numpy as np
import pandas as pd


def count_missing_monthly(dataframe):
    """
        count mising value of column of dataframe

        input: dataframe that index is DATE [yyyy-mm-dd]

        return: dataframe of missing_count in [yyyy-mm, yyyy-mm]
    """
    df = dataframe.isna().astype(int)
    df = df.groupby(pd.Grouper(freq="M")).sum()
    return df


def count_missing_each_month(dataframe):
    """
        count missing value of  data frame of each month [1, 2, ... 12]
        input: dataframe that index is DATE [yyyy-mm-dd]
        return: dataframe of missing_count in [1, 2, ... 12]
    """
    df = dataframe.isna().astype(int)
    df = df.groupby(df.index.month).sum()
    return df
