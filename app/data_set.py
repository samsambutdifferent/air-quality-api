import pandas as pd
import numpy as np

import os


class DataSet:
    def __init__(self, file_path: str):
        self.df = pd.read_parquet(file_path)

    def get_full_data(self) -> str:
        df_with_id = self.df.reset_index().rename(columns={"index": "id"})
        return df_with_id.to_json(orient="records")

    def get_datum_by_id(self, id: int) -> {}:
        return self.df.loc[id] if id in self.df.index else None

    def add_data_entry(self, lat: float, lon: float, gwrpm25: float) -> None:
        self.df.loc[len(self.df)] = {"lat": lat, "lon": lon, "GWRPM25": gwrpm25}
        return len(self.df)

    def update_data_entry(
        self, id: int, lat: float, lon: float, gwrpm25: float
    ) -> None:
        self.df.loc[id] = {"lat": lat, "lon": lon, "GWRPM25": gwrpm25}

    def delete_data_entry(self, id: int) -> None:
        self.df = self.df.drop(id)

    def filter_data(self, lat: float, lon: float) -> str:
        filtered_df = self.df[
            np.isclose(self.df["lat"], lat, atol=1e-9) &
            np.isclose(self.df["lon"], lon, atol=1e-9)
        ]
        df_with_id = filtered_df.reset_index().rename(columns={"index": "id"})
        return df_with_id.to_json(orient="records")

    def get_stats(self) -> {}:
        return {
            "count": int(self.df["GWRPM25"].count()),
            "average": float(self.df["GWRPM25"].mean()),
            "min": float(self.df["GWRPM25"].min()),
            "max": float(self.df["GWRPM25"].max()),
        }
