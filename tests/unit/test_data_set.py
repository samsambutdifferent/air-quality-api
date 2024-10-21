import pytest
import pandas as pd

from app.data_set import DataSet


@pytest.fixture
def mock_dataframe():
    return pd.DataFrame(
        {
            "lat": [-44.355000, -44.355000],
            "lon": [-176.255005, -176.244995],
            "GWRPM25": [6.2, 5.2],
        }
    )


class TestDataSet:
    def test_get_full_data(self, mocker, mock_dataframe):
        mocker.patch("pandas.read_parquet", return_value=mock_dataframe)
        dataset = DataSet(file_path="mock_file_path.parquet")
        result_json = dataset.get_full_data()

        expected_json = (
            '[{"id":0,"lat":-44.355,"lon":-176.255005,"GWRPM25":6.2},'
            '{"id":1,"lat":-44.355,"lon":-176.244995,"GWRPM25":5.2}]'
        )

        assert result_json == expected_json

    def test_get_datum_by_id(self, mocker, mock_dataframe):
        mocker.patch("pandas.read_parquet", return_value=mock_dataframe)
        dataset = DataSet(file_path="mock_file_path.parquet")
        result = dataset.get_datum_by_id(1)

        assert result["lat"] == -44.355
        assert result["lon"] == -176.244995
        assert result["GWRPM25"] == 5.2

    def test_get_datum_by_id_not_found(self, mocker, mock_dataframe):
        mocker.patch("pandas.read_parquet", return_value=mock_dataframe)
        dataset = DataSet(file_path="mock_file_path.parquet")
        result = dataset.get_datum_by_id(3)

        assert result == None

    def test_add_data_entry(self, mocker, mock_dataframe):
        mocker.patch("pandas.read_parquet", return_value=mock_dataframe)
        dataset = DataSet(file_path="mock_file_path.parquet")

        dataset.add_data_entry(
            lat=1.0,
            lon=1.0,
            gwrpm25=1.0,
        )

        assert dataset.df.loc[2]["lat"] == 1.0
        assert dataset.df.loc[2]["lon"] == 1.0
        assert dataset.df.loc[2]["GWRPM25"] == 1.0

    def test_update_data_entry(self, mocker, mock_dataframe):
        mocker.patch("pandas.read_parquet", return_value=mock_dataframe)
        dataset = DataSet(file_path="mock_file_path.parquet")

        dataset.update_data_entry(
            id=0,
            lat=1.0,
            lon=1.0,
            gwrpm25=1.0,
        )

        assert dataset.df.loc[0]["lat"] == 1.0
        assert dataset.df.loc[0]["lon"] == 1.0
        assert dataset.df.loc[0]["GWRPM25"] == 1.0

    def test_delete_data_entry(self, mocker, mock_dataframe):
        mocker.patch("pandas.read_parquet", return_value=mock_dataframe)
        dataset = DataSet(file_path="mock_file_path.parquet")
        dataset.delete_data_entry(id=0)

        assert len(dataset.df) == 1

    def test_filter_data(self, mocker, mock_dataframe):
        mocker.patch("pandas.read_parquet", return_value=mock_dataframe)
        dataset = DataSet(file_path="mock_file_path.parquet")

        result = dataset.filter_data(lat=-44.355000, lon=-176.255005)
        assert result == '[{"id":0,"lat":-44.355,"lon":-176.255005,"GWRPM25":6.2}]'

    def test_stats(self, mocker, mock_dataframe):
        mocker.patch("pandas.read_parquet", return_value=mock_dataframe)
        dataset = DataSet(file_path="mock_file_path.parquet")

        result = dataset.get_stats()

        assert result == {
            "count": int(2),
            "average": float(5.7),
            "min": float(5.2),
            "max": float(6.2),
        }
