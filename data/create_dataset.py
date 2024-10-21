import xarray as xr
import pandas as pd
import numpy as np

file_name = "./data/sdei-global-annual-gwr-pm2-5-modis-misr-seawifs-viirs-aod-v5-gl-04-2000-netcdf/sdei-global-annual-gwr-pm2-5-modis-misr-seawifs-viirs-aod-v5-gl-04-2000-netcdf.nc"

def create_dataset():
    dataset = xr.open_dataset(file_name, chunks={"latitude": 100, "longitude": 1})

    pm25 = dataset["GWRPM25"]

    data_chunks = []

    nan_count = pm25.isnull().sum().values
    total_count = pm25.size

    print(pm25.min().values, pm25.max().values, pm25.mean().values)
    print(f"NaN count: {nan_count}, Total count: {total_count}")

    lat_chunks = list(pm25.chunks[0])
    lon_chunks = list(pm25.chunks[1])

    for i in range(len(lat_chunks)):
        chunk = (lat_chunks[i], lon_chunks[i])
        print(f"chunk count: {i + 1}")
        print(f"chunk shape: {chunk[0], chunk[1]}")
        pm25_chunk = pm25.isel(lat=slice(chunk[0]), lon=slice(chunk[1]))
        nan_mask = np.isnan(pm25_chunk)
        computed_mask = nan_mask.compute()
        valid_data_chunk = pm25_chunk.where(~computed_mask, drop=False)
        df_chunk = valid_data_chunk.to_dataframe().reset_index()
        data_chunks.append(df_chunk)

    final_df = pd.concat(data_chunks, ignore_index=True)
    final_df = final_df[final_df["GWRPM25"].notna()]

    print(f"final df length: {len(final_df)}")
    final_df.to_parquet("./app/pm25_data_final.parquet", index=False)


if __name__=="__main__":
    create_dataset()

