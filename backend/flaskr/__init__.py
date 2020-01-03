import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import text
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import NotFound

from models import db, setup_db, Question, Category
from forms import QuestionForm

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = False
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        return_data = {
            'categories': {}
        }
        for category in categories:
            return_data['categories'][category.id] = category.type
        return jsonify(return_data)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions/<int:question_id>')
    def get_question(question_id):
        question = db.session.query(Question).filter(Question.id == question_id).first()
        if not question:
            return not_found_error()
        return_data = {
            'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'category': question.category,
            'difficulty': question.difficulty,
        }
        return jsonify(return_data)

    @app.route('/questions')
    def get_questions():
        """Get paginated questions (10 per page by default) and by a term filter if present. This permit a simple bookmarkable link for filtered questions"""
        max_per_page = 10
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('perPage', max_per_page, type=int)
        q = db.session.query(Question)
        search_term = request.args.get('searchTerm', None, str)
        if search_term:
            q = q.filter(Question.question.ilike('%{}%'.format(search_term)))  # Filter by term
        questions_pagination = q.paginate(page, per_page, max_per_page)  # Paginate result
        categories = db.session.query(Category).all()
        return_data = {
            'questions': [],
            'total_questions': questions_pagination.total,
            'categories': {},
            'current_category': None,
        }
        for question in questions_pagination.items:
            return_data['questions'].append({
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'category': question.category,
                'difficulty': question.difficulty,
            })
        for category in categories:
            return_data['categories'][category.id] = category.type
        return jsonify(return_data)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = db.session.query(Question).filter(Question.id == question_id).first()
        if not question:
            return not_found_error()
        db.session.delete(question)
        db.session.commit()
        return '', 204

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        form = QuestionForm(MultiDict(mapping=data))
        if not form.validate():
            return bad_request_error(form.errors)
        question = Question(question=form.question.data, answer=form.answer.data, difficulty=form.difficulty.data,
                            category=form.category.data)
        db.session.add(question)
        db.session.commit()
        return_data = {
            'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'difficulty': question.difficulty,
            'category': question.category
        }
        return jsonify(return_data), 201

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions/filters', methods=['POST'])
    def search_question():
        q = db.session.query(Question)
        data = request.get_json()
        if 'searchTerm' not in data:
            return bad_request_error({'error': 'SearchTerm must be passed'})
        q = q.filter(Question.question.ilike('%{}%'.format(data['searchTerm'])))
        questions = q.all()
        questions_data = {
            'questions': [],
            'total_questions': len(questions),
            'current_category': None
        }
        for question in questions:
            questions_data['questions'].append({
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'difficulty': question.difficulty,
                'category': question.category
            })
        return jsonify(questions_data)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        """Get questions by category id"""
        cat = Category.query.filter(Category.id == category_id).first()
        if not cat:
            return not_found_error()
        questions = db.session.query(Question).filter(Question.category == category_id).all()
        questions_data = {
            'questions': [],
            'total_questions': len(questions),
            'current_category': cat.type
        }
        for question in questions:
            questions_data['questions'].append({
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'difficulty': question.difficulty,
                'category': question.category
            })
        return jsonify(questions_data)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        """Get a random question for a quiz"""
        data = request.json
        q = Question.query
        # Filter by category id
        if data['quiz_category']['id']:
            q = q.filter(Question.category == data['quiz_category']['id'])
        q = q.filter(Question.id.notin_(data['previous_questions'])).filter(  # Avoid already done questions
            text('id >= (SELECT FLOOR( MAX(id) * RANDOM()) FROM {} )'.format(Question.__tablename__)))  # Random selection
        question = q.first()
        return_data = {
            'question': {
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'category': question.category,
                'difficulty': question.difficulty
            }
        }
        return jsonify(return_data)

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(400)
    def bad_request_error(error='Bad request'):
        return jsonify({'error': error}), 400

    @app.errorhandler(404)
    def not_found_error(error='Resource not found'):
        if isinstance(error, NotFound):
            return jsonify({'error': str(error)}), 404
        return jsonify({'error': error}), 404

    @app.errorhandler(422)
    def unprocessable_error(error='Unprocessable resource'):
        return jsonify({'error': error}), 422

    @app.errorhandler(500)
    def server_error(error='Server Error'):
        return jsonify({'error': error}), 500

    return app
