from unicodedata import category
from flask import Blueprint, jsonify, abort, request
from models import Category
from utils import paginate

categories = Blueprint('categories', __name__)


@categories.route("/categories")
def retrieve_categories():
    categories_selection = Category.query.order_by(Category.id).all()
    categories = paginate(request, categories_selection, 10)
    if len(categories) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "categories": categories,
            "total_categories": len(categories),
        }
    )
