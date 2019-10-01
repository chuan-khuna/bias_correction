import numpy as np
import pandas as pd


def find_station_grid(observed_lat, observed_lon, model_lats, model_lons):
    """
        find nearest grid center coordinate from station coordinate

        observed lat, lon: station coordinate in lat=[-90..90] lon=[-180..180]

        model lats, lons: model's grid coordinate array (unique)

        return: model's grid center coordinate tuple lon, lat
    """
    model_lats = np.unique(np.array(model_lats))
    model_lons = np.unique(np.array(model_lons))

    lat_diff = np.abs(model_lats - observed_lat)
    lon_diff = np.abs(model_lons - observed_lon)

    min_lat_ind = np.where(lat_diff == min(lat_diff))[0][0]
    min_lon_ind = np.where(lon_diff == min(lon_diff))[0][0]

    grid_lat = model_lats[min_lat_ind]
    grid_lon = model_lons[min_lon_ind]

    return grid_lon, grid_lat

def filter_station(model_lat, model_lon, station_df, grid_step=1.875):
    """
        filter station in side the grid area
    """
    filtered = station_df[
        (np.abs(station_df['LATITUDE'] - model_lat) < grid_step/2) &
        (np.abs(station_df['LONGITUDE'] - model_lon) < grid_step/2)
    ]
    return filtered