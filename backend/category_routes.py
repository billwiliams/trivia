
from flask import Blueprint, jsonify, abort, request
from models import Category


categories = Blueprint('categories', __name__)


@categories.route("/categories")
def retrieve_categories():
    categories_selection = Category.query.order_by(Category.id).all()
    if len(categories_selection) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "categories": {category.id: category.type for category in categories_selection},
            "total_categories": len(categories_selection),
        }
    )
