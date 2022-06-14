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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "What is my name?", "answer": "John Adex", "difficulty": 1, "category": 1}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["categories"], dict))

    def test_404_sent_requesting_category_without_questions(self):
        res = self.client().get("/categories/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(isinstance(data["questions"], list))
        self.assertTrue(data["current_category"])
        self.assertTrue(isinstance(data["categories"], dict))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_question(self):
        res = self.client().delete("/questions/27")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 27).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 26)
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_add_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_405_if_question_addition_not_allowed(self):
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["questions"], list))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_404_sent_requesting_questions_from_invalid_category(self):
        res = self.client().get("/categories/10000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_get_questions_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "world cup"}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(isinstance(data["questions"], list))
        self.assertEqual(len(data["questions"]), 2)
        self.assertTrue(data["current_category"])


    def test_get_questions_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "applejacksmonkey"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 0)
        self.assertTrue(data["current_category"])

    def test_get_quiz_questions_with_previous_questions(self):
        res = self.client().post("/quizzes", json={"previous_questions": [25, 26, 27, 28], "quiz_category": {'id': 1, 'type': "Science"}}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["question"], dict))


    def test_get_quiz_questions_without_previous_questions(self):
        res = self.client().post("/quizzes", json={"previous_questions": [], "quiz_category": {'id': 1, 'type': "Science"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["question"], dict))

    def test_get_quiz_questions_without_category(self):
        res = self.client().post("/quizzes", json={"previous_questions": [1, 4, 20, 15], "quiz_category": {'id': 0, 'type': 'All'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["question"], dict))

    def test_400_play_quiz_with_noInput(self):
        res = self.client().post("/quizzes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()