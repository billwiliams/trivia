from crypt import methods
from flask import Blueprint, jsonify, abort, request
from models import Question, Category
from utils import paginate


questions = Blueprint('questions', __name__)
QUESTIONS_PER_PAGE = 10


@questions.route("/questions")
def retrieve_questions():
    questions_selection = Question.query.order_by(
        Question.id).join(Category, Category.id == Question.category).all()
    print(questions_selection[0])
    questions = paginate(request, questions_selection, QUESTIONS_PER_PAGE)
    categories = [item.type for item in Category.query.all()]
    if len(questions) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "questions": questions,
            "total_questions": len(questions_selection),
            "categories": categories,
            "current_category": 0,
        }
    )


@questions.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()

        return jsonify(
            {
                "success": True,
                "deleted": question_id,

            }
        )

    except:
        abort(422)
