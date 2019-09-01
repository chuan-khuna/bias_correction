import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_missing(dataframe, file_name, title, directory="observed_qc"):
    
    fig = plt.figure(figsize=(10, 6), dpi=120)
    plt.title("{} {}".format(file_name, title))
    try:
        dataframe.index = dataframe.index.strftime("%Y-%m")
        sns.heatmap(dataframe, cmap='Spectral_r')
    except:
        sns.heatmap(
            dataframe,
            cmap='Spectral_r',
            square=True,
        )
    fig.savefig('./{}/{}_{}.png'.format(directory, file_name, title), dpi=120)


def count_missing(datafile, start_date, end_date):
    """
        start_date, end_date: string of date in format 'yyyy-mm-dd'
        
        return: data frame group by monthly [1991-01, 1991-02, ....]
    """
    df = pd.read_csv(datafile)
    df['DATE'] = pd.to_datetime(df['DATE'])
    # filter date
    df = df[(df['DATE'] >= start_date) & (df["DATE"] <= end_date)]
    df.index = df['DATE']
    # check nan in dataframe
    # dataframe is convert to boolean and convert to 0, 1
    df = df.isna().astype(int)
    df = df.groupby(pd.Grouper(freq="M")).sum()
    
    return df

def count_missing_month(datafile, start_date, end_date):
    """
        start_date, end_date: string of date in format 'yyyy-mm-dd'
        
        return: data frame group by month [1, 2, 3 ...12]
    """
    df = pd.read_csv(datafile)
    df['DATE'] = pd.to_datetime(df['DATE'])
    # filter date
    df = df[(df['DATE'] >= start_date) & (df["DATE"] <= end_date)]
    df.index = df['DATE']
    # check nan in dataframe
    # dataframe is convert to boolean and convert to 0, 1
    df = df.isna().astype(int)
    df = df.groupby(df.index.month).sum()
    
    return df

if __name__ == "__main__":
    directory = "./observed/"
    start_date = "1970-01-01"
    end_date = "2005-12-31"
    output_directory = "observed_qc"
    for file_name in os.listdir(directory):
        df = count_missing_month(
            directory+file_name,
            start_date=start_date,
            end_date=end_date
        )
        df = df[['PRCP', 'TAVG', 'TMAX', 'TMIN']]
        if df.shape[0] > 0:
            print(file_name)
            plot_missing(df, file_name, 'month_missing_value', directory=output_directory)