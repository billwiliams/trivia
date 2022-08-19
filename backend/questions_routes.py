from flask import Blueprint, jsonify, abort, request
from models import Question
from utils import paginate


questions = Blueprint('questions', __name__)
QUESTIONS_PER_PAGE = 10


@questions.route("/questions")
def retrieve_questions():
    questions_selection = Question.query.order_by(Question.id).all()
    questions = paginate(request, questions_selection, QUESTIONS_PER_PAGE)
    if len(questions) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "questions": questions,
            "total_questions": len(questions),
        }
    )
