from crypt import methods
import random
from flask import Blueprint, jsonify, abort, request
from models import Question, Category, db
from utils import paginate
import sys


questions = Blueprint('questions', __name__)
QUESTIONS_PER_PAGE = 10

# retrieve questions


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

# Delete a question


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

# Post a new question or search questions


@questions.route('/questions', methods=['POST'])
def create_search_question():
    body = request.get_json()

    new_question = body.get("question", None)
    new_answer = body.get("answer", None)
    new_category = body.get("category", None)
    new_difficulty = body.get("difficulty", None)
    search = body.get("searchTerm", None)

    try:
        if search:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))
            ).all()
            questions = paginate(request, selection, QUESTIONS_PER_PAGE)
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": len(selection),
                    "current_category": [],
                    "categories": {item.id: item.type for item in Category.query.all()},
                }
            )

        else:

            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            return jsonify(
                {
                    "success": True,

                }
            )

    except:
        abort(422)

# Get questions from a category


@questions.route('/categories/<int:category_id>/questions', methods=['GET'])
def retrieve_category_questions(category_id):
    category_questions_selection = Question.query.order_by(
        Question.id).filter(Question.category == category_id).all()

    questions = paginate(
        request, category_questions_selection, QUESTIONS_PER_PAGE)
    categories = {item.id: item.type for item in Category.query.all()}
    if len(questions) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "questions": questions,
            "total_questions": len(category_questions_selection),
            "categories": categories,
            "current_category": [categories[category_id]],
        }
    )

# Get questions for quizz not previously displayed


@questions.route('/quizzes', methods=['POST'])
def play_quizz():
    body = request.get_json()
    quiz_category = body.get("quiz_category", None)
    category = int(quiz_category["id"])
    previous_questions = body.get("previous_questions", None)

    try:
        if category == 0:
            questions_not_displayed = Question.query.order_by(
                Question.id).filter(
                Question.id.not_in(previous_questions)).all()
        else:

            questions_not_displayed = Question.query.order_by(
                Question.id).filter(Question.category == category).filter(
                    Question.id.not_in(previous_questions)).all()
        if len(questions_not_displayed) == 0:
            return jsonify(
                {
                    "success": True,
                    "forceEnd": True,

                })
        question = random.choice(questions_not_displayed)
        question = question.format()
        return jsonify(
            {
                "success": True,
                "question": question,

            }
        )

    except:
        print(sys.exc_info())
        abort(422)
