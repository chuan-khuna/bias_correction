import pandas as pd
import os

csv_folders = [
    "./observed_qc/inconsistency/",
    "./observed_qc/outlier/TAVG/",
    "./observed_qc/outlier/TMAX/",
    "./observed_qc/outlier/TMIN/"
]

output_files = [
    "./observed_qc/summary_qc/inconsistency.csv",
    "./observed_qc/summary_qc/TAVG_outlier.csv",
    "./observed_qc/summary_qc/TMAX_outlier.csv",
    "./observed_qc/summary_qc/TMIN_outlier.csv"
]

def concat_csv():
    for i in range(len(csv_folders)):
        folder = csv_folders[i]
        df_list = []
        for f in os.listdir(folder):
            print(f"{i} \t {f}")
            df_list.append(pd.read_csv(folder+f))
        concat = pd.concat(df_list)
        concat.to_csv(output_files[i], index=False)

if __name__ == "__main__":
    concat_csv()