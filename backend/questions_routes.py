from crypt import methods
from flask import Blueprint, jsonify, abort, request
from models import Question, Category, db
from utils import paginate
import sys


questions = Blueprint('questions', __name__)
QUESTIONS_PER_PAGE = 10


@questions.route("/questions")
def retrieve_questions():
    questions_selection = Question.query.order_by(
        Question.id).join(Category, Category.id == Question.category).all()

    questions = paginate(request, questions_selection, QUESTIONS_PER_PAGE)
    categories = {item.id: item.type for item in Category.query.all()}
    if len(questions) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "questions": questions,
            "total_questions": len(questions_selection),
            "categories": categories,
            "current_category": [],
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


@questions.route('/questions', methods=['POST'])
def create_search_question():
    body = request.get_json()

    new_question = body.get("question", None)
    new_answer = body.get("answer", None)
    new_category = body.get("category", None)
    new_difficulty = body.get("difficulty", None)
    search = body.get("search", None)

    try:
        if search:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))
            )
            current_questions = paginate(
                request, selection, QUESTIONS_PER_PAGE)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection.all()),
                }
            )

        else:
            print(new_question)
            print(new_answer)
            print(new_category)
            print(new_difficulty)
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            print(sys.exc_info())

            return jsonify(
                {
                    "success": True,

                }
            )

    except:
        abort(422)
