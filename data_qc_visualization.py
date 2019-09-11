import numpy as np
import pandas as pd
import os

# my lib
import my_data_qc_lib.count_missing as count_missing
import my_data_qc_lib.plot_missing_heatmap as plot_missing_heatmap
import my_data_qc_lib.plot_box_dist as plot_box_dist

temp_ind = ["TAVG", "TMAX", "TMIN"]
prcp_ind = ["PRCP"]
start_date = "1970-01-01"
end_date = "2005-12-31"
date_col = "DATE"

csv_directory = "./observed/"
csv_files = os.listdir(csv_directory)

for f in csv_files:

    print(f"{f}")

    # remove .csv
    title = f[:-4]

    df = pd.read_csv(csv_directory + f)
    # convert date column to datetime
    df[date_col] = pd.to_datetime(df[date_col])
    # select date in interested range
    df1 = df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]
    # assign date column as index
    df1.index = df1[date_col]

    if df1.shape[0] > 0:
        monthly_missing = count_missing.count_missing_monthly(df1[prcp_ind + temp_ind])
        month_missing = count_missing.count_missing_each_month(df1[prcp_ind + temp_ind])
        plot_missing_heatmap.plot_missing_heatmap(
            monthly_missing,
            title + "_monthly_missing",
            "./observed_qc/missing_value/monthly/",
        )
        plot_missing_heatmap.plot_missing_heatmap(
            month_missing,
            title + "_month_missing",
            "./observed_qc/missing_value/month/",
        )

        plot_box_dist.box_and_hist_plot(
            df1.dropna(),
            temp_ind,
            xlabel="temperature",
            title=title,
            directory="./observed_qc/box_dist/temperature/"
        )
        plot_box_dist.box_and_hist_plot(
            df1.dropna(),
            prcp_ind,
            xlabel="PRCP",
            title=title,
            directory="./observed_qc/box_dist/prcp/"
        )
