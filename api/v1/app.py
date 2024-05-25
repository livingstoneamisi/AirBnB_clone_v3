#!/usr/bin/python3
"""Flask instance implementation."""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    storage.close()


@app.errorhandler(404)
def error(exc):
    return({
            "error": "Not found"
            }, 404)


if __name__ == "__main__":
    from os import getenv
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True)