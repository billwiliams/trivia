import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_user = 'postgres'
        self.database_pass = 'abc'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.database_user, self.database_pass, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {"question": "Best Country in Africa?",
                             "answer": "Kenya", "category": 1, "difficulty": 4}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Categories Tests

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(len(data["categories"]))

    def test_404_sent_request_for_wrong_enpoint(self):
        res = self.client().get("/categores")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # Categories Tests

    # Questions Tests

    def test_get_quetions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_paginated_questions(self):
        res = self.client().get("/questions?page=110000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # Questions Tests

    # delete question ->change id when running multiple times since test fails if book already deleted
    def test_delete_question(self):
        res = self.client().delete("/questions/6")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 6)

        self.assertEqual(question, None)

    def test_422_if_book_does_not_exist(self):
        res = self.client().delete("/questions/1200")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Post Questions
    def test_create_new_question(self):

        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_405_if_book_creation_not_allowed(self):
        res = self.client().post("/questions/13", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # Category Questions Test

    def test_get_category_quetions(self):
        res = self.client().get("categories/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["current_category"]))

    def test_404_sent_requesting_questions_from_non_existence_category(self):
        res = self.client().get("/categories/questions/2220000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # Category Questions Test

    def test_get_quizz_quetions(self):
        res = self.client().post(
            "/quizz", json={"category": 1, "previous_questions": [20, 21]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["current_category"]))

    def test_422_sent_requesting_quizz_from_non_existence_category(self):
        res = self.client().post(
            "/quizz", json={"category": 30, "previous_questions": [20, 21]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_405_sent_requesting_quizz_from_with_non_allowable_method(self):
        res = self.client().patch(
            "/quizz", json={"category": 3, "previous_questions": [20, 21]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
