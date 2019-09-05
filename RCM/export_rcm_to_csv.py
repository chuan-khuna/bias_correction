import numpy as np
import pandas as pd
import os
from datetime import datetime, date, timedelta
from netCDF4 import Dataset


def mask_coordinate_index(coor_arr, min_val, max_val):
    """
        return: array of index that coordinate in range [min_val, max_val]
    """
    coor_index = np.where((min_val <= coor_arr) & (coor_arr <= max_val))
    return coor_index[0]

def convert_time_offset_to_datetime(offset_arr, start_date):
    """
        convert time offset
            example: 10 day sine 1997-01-31

        start_date: date in string format yyyy-mm-dd

        return: datetime string array in string format yyyy-mm-dd
    """
    dates = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    for offset in offset_arr:
        date = start_date + timedelta(offset)
        dates.append(date.strftime("%Y-%m-%d"))
    return dates


def export_nc_to_csv(directory, min_lon, max_lon, min_lat, max_lat, output_filename):

    df_arr = []

    for file_name in os.listdir(directory):
        ds = Dataset(directory+file_name)
        print(f"File: {file_name}")
        # calculate date
        offsets = np.array(ds['time'][:])
        start_date = "1850-01-01"
        dates = convert_time_offset_to_datetime(offsets, start_date)

        lats = np.array(ds['lat'][:])
        lons = np.array(ds['lon'][:])
        # shift lon
        lons = np.roll(lons, int(len(lons)/2))
        lons[:int(len(lons)/2)] -= 360
        # get masked coordinate index
        mask_lat = mask_coordinate_index(lats, min_lat, max_lat)
        mask_lon = mask_coordinate_index(lons, min_lon, max_lon)
        min_lat_ind, max_lat_ind = mask_lat[0], mask_lat[-1]
        min_lon_ind, max_lon_ind = mask_lon[0], mask_lon[-1]

        indices = ['tas', 'tasmin', 'tasmax', 'pr']
        data = []
        # shift data
        for index in indices:
            raw = np.array(ds[index][:])
            # shift data at axis 2 (lon axis)
            shifted = np.roll(raw, int(raw.shape[2]/2), axis=2)
            # select shifted data
                # all of date axis, and coordinate is in lat/lon limit
            data.append(shifted[:, min_lat_ind:max_lat_ind+1, min_lon_ind:max_lon_ind+1])

        for i in range(len(mask_lat)):
            for j in range(len(mask_lon)):
                df = pd.DataFrame({
                    "date": dates,
                    "lat": [lats[mask_lat[i]]] * len(dates),
                    "lon": [lons[mask_lon[j]]] * len(dates),
                    "tas": data[0][:, i, j],
                    "tasmin": data[1][:, i, j],
                    "tasmax": data[2][:, i, j],
                    "pr": data[3][:, i, j]
                })

                # round
                df = df.round({"lat": 5, "lon": 3, "tas": 5, "tasmin": 5, "tasmax": 5, "pr": 5})
                df_arr.append(df)
    concat_df = pd.concat(df_arr)
    print(f"concatenated dataframe shape {concat_df.shape}")
    concat_df.to_csv(output_filename, index=False)

if __name__ == "__main__":
    # TH lon +95E to +110E -> lon = (95, 110)
    # TH lat +25N to +5N -> lat = (5, 25)
    types = ["hist", "rcp45", "rcp85"]
    t = types[0]
    export_nc_to_csv(f'./MPI-ESM-MR/{t}/', 80, 115, -5, 30, f"RCM_{t}_TH.csv")