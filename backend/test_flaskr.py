import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import db, setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('config_test')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_user = "postgres:password"
        self.database_path = "postgresql://{}@{}/{}".format(self.database_user, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            # self.db = SQLAlchemy()
            # self.db.init_app(self.app)
            # # create all tables
            # self.db.create_all()
            self.db = db
            self.questions_id_to_delete = []
            self.categories_id_to_delete = []

    def tearDown(self):
        """Executed after reach test. Deleting models created to test"""
        Question.query.filter(Question.id.in_(self.questions_id_to_delete)).delete(synchronize_session=False)
        self.questions_id_to_delete = []
        self.db.session.query(Category).filter(Category.id.in_(self.categories_id_to_delete)).delete(synchronize_session=False)
        self.categories_id_to_delete = []
        self.db.session.commit()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_question_create(self):
        json_data = {'question': 'What is the best question?', 'answer': 'This', 'category': 'test', 'difficulty': 2}
        res = self.client().post('/questions', json=json_data)
        data = json.loads(res.data)
        test_question = self.db.session.query(Question).filter(
            (Question.question == 'What is the best question?') &
            (Question.answer == 'This') &
            (Question.category == 'test')).first()
        self.assertIsNotNone(test_question)
        self.questions_id_to_delete.append(test_question.id)
        self.assertEqual(res.status_code, 201)  # 201 code for 'Resource Created'
        self.assertEqual(data['question'], 'What is the best question?')
        self.assertEqual(data['answer'], 'This')
        self.assertEqual(data['category'], 'test')
        self.assertEqual(data['difficulty'], 2)

    def test_question_list(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_question_read(self):
        question = self.db.session.query(Question).first()
        res = self.client().get('/questions/{}'.format(question.id))
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question'], question.question)
        self.assertEqual(data['answer'], question.answer)
        self.assertEqual(data['category'], question.category)
        self.assertEqual(data['difficulty'], question.difficulty)

    def test_question_edit(self):
        test_question = Question(question='Is a test?', answer='yes', category='test', difficult=1)
        self.db.session.add(test_question)
        self.db.session.commit()
        self.questions_id_to_delete.append(test_question.id)
        edit_fields = {
            'question': 'Is this q. edited?',
            'answer': 'Sure',
            'difficult': 2,
            'category': 'edit_test'
        }
        res = self.client().patch('/questions/{}'.format(test_question.id), json=edit_fields)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question'], edit_fields['question'])
        self.assertEqual(data['answer'], edit_fields['answer'])
        self.assertEqual(data['category'], edit_fields['category'])
        self.assertEqual(data['difficulty'], edit_fields['difficulty'])

    def test_question_delete(self):
        test_question = Question(question='Is a test?', answer='yes', category=1, difficulty=1)
        self.db.session.add(test_question)
        self.db.session.commit()
        self.questions_id_to_delete.append(test_question.id)
        res = self.client().delete('/questions/{}'.format(test_question.id))
        test_question = self.db.session.query(Question).filter(Question.id == test_question.id).first()
        self.assertEqual(res.status_code, 204)
        self.assertIsNone(test_question)

    def test_category_create(self):
        json_data = {'type': 'Test'}
        res = self.client().post('/categories', json=json_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)  # 201 code for 'Resource Created'
        test_category = self.db.session.query(Category).filter(
            (Category.id == data['id'])).first()
        self.assertIsNotNone(test_category)
        self.categories_id_to_delete.append(test_category.id)
        self.assertEqual(data['type'], 'Test')

    def test_category_list(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_category_read(self):
        cat = self.db.session.query(Category).first()
        res = self.client().get('/categories/{}'.format(cat.id))
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['type'], cat.type)

    def test_category_edit(self):
        test_category = Question(type='Test')
        self.db.session.add(test_category)
        self.db.session.commit()
        self.categories_id_to_delete.append(test_category.id)
        edit_fields = {
            'type': 'Edit Test'
        }
        res = self.client().patch('/categories/{}'.format(test_category.id), json=edit_fields)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['type'], edit_fields['type'])

    def test_category_delete(self):
        test_category = Category(type='Test')
        self.db.session.add(test_category)
        self.db.session.commit()
        self.categories_id_to_delete.append(test_category.id)
        res = self.client().delete('/categories/{}'.format(test_category.id))
        test_question = self.db.session.query(Category).filter(Question.id == test_category.id).first()
        self.assertEqual(res.status_code, 204)
        self.assertIsNone(test_category)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
