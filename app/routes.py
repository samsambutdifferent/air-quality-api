from flask import Blueprint, current_app, jsonify, request, make_response
from flask.wrappers import Response

from .logger import setup_logger

import logging
import os

main_bp = Blueprint("main", __name__)
logger = setup_logger(name="routes", log_file="routes.txt", level=logging.DEBUG)


@main_bp.route("/data", methods=["GET"])
def get_data() -> Response:
    """Retrieve all available data."""
    try:
        result = current_app.data_set.get_full_data()
        return Response(result, status=200)
    except AttributeError as e:
        logger.error(f"Error for get data: {e}")
        return Response("Internal error", status=500)


@main_bp.route("/data/<int:id>", methods=["GET"])
def get_datum_by_id(id: int) -> Response:
    """Fetch a specific datum by its ID."""
    try:
        datum = current_app.data_set.get_datum_by_id(id)
        if datum is not None:
            return jsonify(datum.to_dict()), 200
        else:
            return Response("Item not found", status=404)
    except AttributeError as e:
        logger.error(f"Error for get datum by id: {e}")
        return Response("Internal error", status=500)


@main_bp.route("/data", methods=["POST"])
def post_data() -> Response:
    """Add a new data entry (validate required fields)."""
    try:
        data = request.get_json()
        lat = float(data["lat"])
        lon = float(data["lon"])
        gwrpm25 = float(data["gwrpm25"])
        updated_id = current_app.data_set.add_data_entry(
            lat=lat, lon=lon, gwrpm25=gwrpm25
        )
        return Response(f"success new entry id: {updated_id}", 201)
    except (KeyError, TypeError, ValueError) as e:
        return (
            jsonify(
                {
                    "error": "Invalid input, lat, lon, and gwrpm25 are required and must be floats."
                }
            ),
            400,
        )
    except AttributeError as e:
        logger.error(f"Error for post data: {e}")
        return Response("Internal error", status=500)


@main_bp.route("/data/<int:id>", methods=["PUT"])
def put_datum_by_id(id: int) -> Response:
    """Update an existing data entry."""
    try:
        if current_app.data_set.get_datum_by_id(id) is None:
            return jsonify({"error": f"Entry with ID {id} not found."}), 404

        data = request.get_json()
        lat = float(data["lat"])
        lon = float(data["lon"])
        gwrpm25 = float(data["gwrpm25"])
        current_app.data_set.update_data_entry(id=id, lat=lat, lon=lon, gwrpm25=gwrpm25)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Entry with ID {id} updated successfully.",
                }
            ),
            200,
        )
    except (KeyError, TypeError, ValueError):
        return (
            jsonify(
                {
                    "error": "Invalid input, lat, lon, and gwrpm25 are required and must be floats."
                }
            ),
            400,
        )
    except AttributeError as e:
        logger.error(f"Error for put datum by id: {e}")
        return Response("Internal error", status=500)


@main_bp.route("/data/<int:id>", methods=["DELETE"])
def delete_datum_by_id(id: int) -> Response:
    """Delete a data entry."""
    try:
        if current_app.data_set.get_datum_by_id(id) is None:
            return jsonify({"error": f"Entry with ID {id} not found."}), 404

        current_app.data_set.delete_data_entry(id=id)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Entry with ID {id} deleted successfully.",
                }
            ),
            200,
        )
    except (KeyError, TypeError, ValueError):
        return (
            jsonify(
                {
                    "error": "Invalid input, lat, lon, and gwrpm25 are required and must be floats."
                }
            ),
            400,
        )
    except AttributeError as e:
        logger.error(f"Error for delete data entry by id: {e}")
        return Response("Internal error", status=500)


@main_bp.route("/data/filter/<string:lat>/<string:long>", methods=["GET"])
def get_filtered_data(lat: str, long: str) -> Response:
    """Filter the dataset based on latitude and longitude up to 1e-9 floating point precision."""
    try:
        # convert to float as negative not handled natively
        lat = float(lat)
        long = float(long)

        result = current_app.data_set.filter_data(lat=lat, lon=long)

        return Response(result, status=200)
    except ValueError:
        return jsonify({"error": "Invalid latitude or longitude format."}), 400
    except AttributeError as e:
        logger.error(f"Error for filter data: {e}")
        return Response("Internal error", status=500)


@main_bp.route("/data/stats", methods=["GET"])
def get_stats() -> Response:
    """Provide basic statistics (count, average PM2.5, min, max) across the dataset"""
    try:
        results = current_app.data_set.get_stats()
        return jsonify(results), 200
    except AttributeError as e:
        logger.error(f"Error for get stats: {e}")
        return Response("Internal error", status=500)
