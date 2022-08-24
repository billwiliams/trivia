import os
from sqlite3 import dbapi2
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from error_routes import errors
from category_routes import categories
from questions_routes import questions

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # Error routes
    app.register_blueprint(errors)
    # Category routes
    app.register_blueprint(categories)
    # Questions Routes
    app.register_blueprint(questions)

    setup_db(app)
    CORS(app)
    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # adding this error due to project rubric which states one to use @app.errorhandler
    # otherwise all other errors in error_routes.py blueprint file

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False,
                    "error": 500,
                     "message": "Internal server error"}),
            500,

        )

    return app
