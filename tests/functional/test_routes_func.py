import json

import pytest
import pandas as pd
from flask import current_app

from app import create_app
from app.data_set import DataSet


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def dataset():
    data = pd.DataFrame(
        {
            "lat": [44.355000, -44.2222],
            "lon": [176.255005, -176.2222],
            "GWRPM25": [6.2, 5.2],
        }
    )

    dataset = DataSet.__new__(DataSet)
    dataset.df = data
    return dataset


class TestGetDataRoute:
    def test_get_data_success(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.get("/data")
            expected = (
                '[{"id":0,"lat":44.355,"lon":176.255005,"GWRPM25":6.2},'
                '{"id":1,"lat":-44.2222,"lon":-176.2222,"GWRPM25":5.2}]'
            )

            assert response.status_code == 200
            assert response.data.decode("utf-8") == expected

    def test_get_data_fail(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            response = client.get("/data")

            assert response.status_code == 500


class TestGetDatumByIdRoute:
    def test_get_datum_by_id_success(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.get(f"/data/{1}")
            data = json.loads(response.data.decode("utf-8"))

            assert response.status_code == 200
            assert data == {"GWRPM25": 5.2, "lat": -44.2222, "lon": -176.2222}

    def test_get_datum_by_id_not_found(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.get(f"/data/{999}")

            assert response.status_code == 404

    def test_get_datum_by_id_fail(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            response = client.get(f"/data/{1}")

            assert response.status_code == 500

    def test_get_datum_by_id_fail_wrong_input(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            response = client.get(f"/data/{'hello'}")

            assert response.status_code == 404


class TestPostData:
    def test_post_data_success(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            data = {"lat": 40.7128, "lon": 74.0060, "gwrpm25": 12.5}
            response = client.post(
                "/data", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 201

    def test_post_data_fail(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            data = {"lat": 40.7128, "lon": 74.0060, "gwrpm25": 12.5}
            response = client.post(
                "/data", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 500

    def test_post_data_success_type_change(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            data = {"lat": "40.7128", "lon": 74.0060, "gwrpm25": 12.5}
            response = client.post(
                "/data", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 201

    def test_post_data_fail_type_change(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            data = {"lat": "hello", "lon": 74.0060, "gwrpm25": 12.5}
            response = client.post(
                "/data", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 400


class TestPutData:
    def test_put_datum_by_id_success(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            data = {"lat": 1.0, "lon": 1.0, "gwrpm25": 1.0}
            response = client.put(
                f"/data/{0}", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 200
            assert current_app.data_set.df.loc[0]["lat"] == 1.0
            assert current_app.data_set.df.loc[0]["lon"] == 1.0
            assert current_app.data_set.df.loc[0]["GWRPM25"] == 1.0

    def test_put_datum_by_id_fail(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            data = {"lat": 1.0, "lon": 1.0, "gwrpm25": 1.0}
            response = client.put(
                f"/data/{0}", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 500

    def test_put_datum_by_id_success_type_change(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            data = {"lat": "1.0", "lon": 1.0, "gwrpm25": 1.0}
            response = client.put(
                f"/data/{0}", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 200
            assert current_app.data_set.df.loc[0]["lat"] == 1.0
            assert current_app.data_set.df.loc[0]["lon"] == 1.0
            assert current_app.data_set.df.loc[0]["GWRPM25"] == 1.0

    def test_put_datum_by_id_fail_type_change(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            data = {"lat": "hello", "lon": 1.0, "gwrpm25": 1.0}
            response = client.put(
                f"/data/{0}", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 400

    def test_put_datum_by_id_fail_id_type(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            data = {"lat": 1.0, "lon": 1.0, "gwrpm25": 1.0}
            response = client.put(
                f"/data/hello", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 404


class TestDeleteData:
    def test_delete_data_success(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.delete(f"/data/{0}")

            assert response.status_code == 200
            assert 0 not in current_app.data_set.df.index

    def test_delete_data_fail(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            response = client.delete(f"/data/{0}")
            assert response.status_code == 500

    def test_put_datum_by_id_fail_id_type(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.delete(f"/data/{'hello'}")
            assert response.status_code == 404


class TestFilterData:
    def test_filter_data_success(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.get(f"/data/filter/44.355/176.255005")
            assert response.status_code == 200
            assert (
                response.data.decode("utf-8")
                == '[{"id":0,"lat":44.355,"lon":176.255005,"GWRPM25":6.2}]'
            )

    def test_filter_data_success_negative(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.get(f"/data/filter/-44.2222/-176.2222")
            assert response.status_code == 200
            assert (
                response.data.decode("utf-8")
                == '[{"id":1,"lat":-44.2222,"lon":-176.2222,"GWRPM25":5.2}]'
            )

    def test_filter_data_not_found(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.get(f"/data/filter/1.0/1.0")
            assert response.status_code == 200
            assert response.data.decode("utf-8") == "[]"

    def test_filter_data_fail_type(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            response = client.get(f"/data/filter/hello/1.0")
            assert response.status_code == 400

    def test_filter_data_fail(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            response = client.get(f"/data/filter/1.0/1.0")
            assert response.status_code == 500


class TestGetStats:
    def test_get_stats_success(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = dataset
            response = client.get("/data/stats")
            assert response.status_code == 200
            assert json.loads(response.data.decode("utf-8")) == {
                "average": 5.7,
                "count": 2,
                "max": 6.2,
                "min": 5.2,
            }

    def test_get_stats_fail(self, client, app, dataset):
        with app.app_context():
            current_app.data_set = None
            response = client.get("/data/stats")
            assert response.status_code == 500
