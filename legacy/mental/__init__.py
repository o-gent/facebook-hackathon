"""
__init__.py -> Handle the flask app creation
"""

from flask import Flask

from mental.config import Config
from mental.views import index
from mental.logger import setup_logger

logger = setup_logger('mental-__init__', 'mental-__init__.log')

def create_app():
    """
    Create the flask app instance
    """

    app = Flask(__name__)
    app.config.from_object(Config)

    # register routes
    app.add_url_rule("/", "index", index, methods=["GET"])

    return app
