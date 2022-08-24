# Backend - Trivia API
This project is a quizz trivia game.User can play the game  based on certain categories or general questions with the ability to show  answers.The game provides five questions of the chosen category then ends. If a category has less than five questions, the gane ends when all  the questions are displayed.On finishing the game the user is shown the final score. Questions shown to the user are selected at random and the user   can add or delete questions from the database.

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server


#### Backend
To run the application navigate to the backend folder and  run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 


#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: bad request
- 404: resource not found
- 422: not processable 
- 405: method not allowed
- 500: Internal server error

### Endpoints 

#### `GET '/categories'`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- `curl http://127.0.0.1:5000/categories` 

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### GET /questions
-Fetches  a  paginated list of question objects, a dictionary of  categories, current categories list and total number of questions  
- Request Arguments: page starting from 1. 
- Returns: A  paginated list of question objects in groups of  10, success value,  total number of questions,categories list and current category
- curl http://127.0.0.1:5000/questions` 
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": [],
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
   "success": true,
  "total_questions": 24
}
```
#### POST /questions
- Creates a new question using the submitted question, answer, difficulty and rating.
- Request Arguments: a json object with question, answer, difficulty and rating values . 
- Returns: success value
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"which is largest lake in Africa", "answer":"Tangayika","difficulty":2, "rating":5}'`
``` json
{
  "success": true
}
```

#### POST /questions
- Searches questions that has the provided Phrase 
- Request Arguments: a dictionary with the searchTerm value. 
- Returns: A  paginated list of question objects in groups of  10 matching the searchTerm phrase, success value,  total number of questions,categories list and current category
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":" Tom"}'`
``` json
{
  {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": [],
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 1
}
}
```

### GET /categories/{category_id}/questions
-Fetches   question  related to a given category  
- Request Arguments: category id an integer relating to a certain category 
- Returns: A  paginated list of question objects related to the requested category , success value,  total number of questions,categories list and current category requested
-`curl http://127.0.0.1:5000/categories/5/questions` 
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": [
    "Entertainment"
  ],
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### DELETE /questions/{question_id}
-Deletes the question of the given ID if it exists. ,  
- Request Arguments: question id an integer relating to a certain question 
- Returns:  the id of the deleted question, success value

- `curl -X DELETE http://127.0.0.1:5000/question/5`
```json
{
  "deleted": 5,
  "success": true
}

```

#### POST /quizzes
- Fetches for a  random question that has not been previously seen based on given category 
- Request Arguments: a dictionary with the previous questions list and  quiz category with id of a given category.  a category id value of 0 indicates all categories
- Returns: A  random question exclusive of the previous 
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"id":1} ,"previous_questions":[2]}'`
``` json
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```


## Deployment N/A

## Authors
Yours truly, Wilson Ndirangu

## Acknowledgements 
The awesome team at Udacity. 

