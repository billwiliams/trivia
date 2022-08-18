from unicodedata import category
from flask import Blueprint, jsonify, abort
from models import Category

categories = Blueprint('categories', __name__)


@categories.route("/categories")
def retrieve_categories():
    categories_selection = Category.query.order_by(Category.id).all()
    categories = [category.format() for category in categories_selection]
    if len(categories) == 0:
        abort(400)

    return jsonify(
        {
            "success": True,
            "categories": categories,
            "total_categories": len(categories),
        }
    )
