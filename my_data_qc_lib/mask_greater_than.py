import numpy as np
import pandas as pd

def greater_than(dataframe, col1, col2):
    """
        select row in data frame if col1 > col2

        dataframe: dataframe dropped nan
        return dataframe
    """

    df = dataframe[dataframe[col1] > dataframe[col2]]
    return df