# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Flask-WTForm](https://flask-wtf.readthedocs.io/en/stable/#) is an extension to check form request data and have an easy way to create forms

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Endpoints

- ### GET /categories
    Endpoint to retrieve all available categories as a dictionary of category_id => category_type.
    
    Example of JSON response:
    ```
    {
        1: 'Sport',
        2: 'Cinema',
        3: 'Games',
        4: 'Science',
        ...
    }
    ```


- ### GET /questions
    Get the list of paginated questions (by default 10 questions per page). Is possible to search specific questions by the searchTerm query parameter.
    
    Query Parameters:
    - **page**: Number of questions page to retrieve. Response with a 404 if the page number is over the last available page
    - **perPage**: Optional Integer. If passed specify the number of question per page. Max 20 per page
    - **searchTerm**: String to search questions by question text. The research is _case insensitive_

    GET URL request example to get first page of questions containing word _Which_:
    ```
    /questions?page=1&searchTerm=Which
    ```

    Response example:
    ```
    {
    "questions": [
        {
          "answer": "Maya Angelou", 
          "category": 4, 
          "difficulty": 2, 
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
          "answer": "Muhammad Ali", 
          "category": 4, 
          "difficulty": 1, 
          "id": 9, 
          "question": "What boxer's original name is Cassius Clay?"
        }, 
        ...
      ], 
      "total_questions": 21, <== Number of TOTAL questions, not only questions in this response
      "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        ...
      }, 
      "current_category": null
    }
    
    ```
    
- ### POST /questions
    Create a new question. Return a **201** if request is completed with success.
    
    JSON Parameters:
    - **question**: String. Question text
    - **answer**: String. Answer to the question
    - **difficulty**: Integer. Difficulty of the question
    - **category**: Id of the category which question belongs
    
    Request example:
    ```
    {
        question: "Is a new question?",
        answer: "Yes",
        difficulty: 4,
        category: 1
    }
    ```
  
    The successful request return the created resource. Response example:
    ```
    {
        question: "Is a new question?",
        answer: "Yes",
        difficulty: "4",
        category: 1
    }
    ```

- ### DELETE /questions/<question_id>
    Delete a question specifying the ID on url. Return a 204 HTTP status if request is completed
    
    **URL** Parameters:
    - **question_id**: Id of question to delete

- ### POST /quizzes
    Get the list of paginated questions (by default 10 questions per page). Is possible to search specific questions by the searchTerm query parameter.
    
    **JSON** Body Parameters:
    - **previous_questions**: Array. List of question id that has been already done to avoid question repetitions
    - **quiz_category**: Optional Integer. If passed specify the number of question per page. Max 20 per page
    - **quiz_category.id**: Id of category of wanted questions. Pass 0 if you want questions of any category
    - **quiz_category.type**: Textual name of wanted category
    
    Request example:
    ```
    {
        "previous_questions":[2, 4],
        "quiz_category": {
            "type":"Science",
            "id":"1"
        }
    }
    ```
    
    Response example:
    ```
    {
      "question": {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
      }
    }
    ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```