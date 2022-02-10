#!/usr/bin/python3
<<<<<<< HEAD
"""app"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_call(self):
    """call"""
=======
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
>>>>>>> ca3c23b7c7c40809fa756105a35f50791fa28820
    storage.close()


@app.errorhandler(404)
<<<<<<< HEAD
def error_found(e):
    """found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0'

    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT is None:
        HBNB_API_PORT = '5000'

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
=======
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
>>>>>>> ca3c23b7c7c40809fa756105a35f50791fa28820
