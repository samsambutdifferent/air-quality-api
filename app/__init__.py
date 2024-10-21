from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from .data_set import DataSet

import os

FILE_NAME = "pm25_data_final.parquet"


def create_app():
    app = Flask(__name__)
    # NOTE this is only enabled globally for dev purposes
    CORS(app)

    from .routes import main_bp

    app.register_blueprint(main_bp)

    SWAGGER_URL = "/api"
    API_URL = "/static/swagger.json"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Air Quality Api"}
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    file_path = os.path.join(app.root_path, "./", FILE_NAME)
    data_set = DataSet(file_path)
    app.data_set = data_set

    return app
