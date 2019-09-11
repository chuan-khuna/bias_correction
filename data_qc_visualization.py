import numpy as np
import pandas as pd
import os

# my lib
import my_data_qc_lib.count_missing as count_missing
import my_data_qc_lib.plot_missing_heatmap as plot_missing_heatmap
import my_data_qc_lib.plot_box_dist as plot_box_dist
import my_data_qc_lib.mask_greater_than as mask_err
import my_data_qc_lib.mask_outlier as mask_outlier

temp_ind = ["TAVG", "TMAX", "TMIN"]
prcp_ind = ["PRCP"]
start_date = "1970-01-01"
end_date = "2005-12-31"
date_col = "DATE"

csv_directory = "./observed/"
csv_files = os.listdir(csv_directory)


def visualize():
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

        if not (df1.empty):
            monthly_missing = count_missing.count_missing_monthly(
                df1[prcp_ind + temp_ind]
            )
            month_missing = count_missing.count_missing_each_month(
                df1[prcp_ind + temp_ind]
            )
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
                directory="./observed_qc/box_dist/temperature/",
            )
            plot_box_dist.box_and_hist_plot(
                df1.dropna(),
                prcp_ind,
                xlabel="PRCP",
                title=title,
                directory="./observed_qc/box_dist/prcp/",
            )


def mask_csv():
    for f in csv_files:
        # remove .csv
        title = f[:-4]

        df = pd.read_csv(csv_directory + f)
        # convert date column to datetime
        df[date_col] = pd.to_datetime(df[date_col])
        # select date in interested range
        df1 = df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]
        df1 = df1.dropna()

        print(f"{f}")

        # mask error value
        tavg_tmax = mask_err.greater_than(df1, "TAVG", "TMAX")
        tmin_tavg = mask_err.greater_than(df1, "TMIN", "TAVG")
        tmin_tmax = mask_err.greater_than(df1, "TMIN", "TMAX")
        concat_err = pd.concat([tavg_tmax, tmin_tavg, tmin_tmax])

        output_directory = "./observed_qc/error_val/"

        if not (concat_err.empty):
            concat_err["DATE"] = pd.to_datetime(concat_err["DATE"])
            concat_err = concat_err.sort_values(by=["DATE"])
            concat_err = concat_err.drop_duplicates()
            concat_err.to_csv(output_directory + f, index=False)

        output_directory = "./observed_qc/outlier/"
        for ind in temp_ind:
            outlier = mask_outlier.mask_outlier_by_std(df1, ind)
            if not (outlier.empty):
                outlier.to_csv(f"{output_directory}{ind}/{f}", index=False)


if __name__ == "__main__":
    visualize()
    mask_csv()
