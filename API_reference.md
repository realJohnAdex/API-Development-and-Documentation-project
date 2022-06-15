## API Reference

### Getting Started
- This software can only be launched locally at the moment and is not available as a base URL. The default location for the backend app is, `http://127.0.0.1:5000/`, it is configured as a proxy in the frontend. 
- Authentication: Authentication or API keys are not required in this version of the application. 

### Error Handling
Errors are returned in the following format as JSON objects:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
When requests fail, the API will return four errors types:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable  

### Endpoints 
#### GET '/categories'

- Retrieves a dictionary of categories, where the keys are the ids and the value is the category's matching string.
- Arguments for Requests: None
- Returns: A single-key object, categories, that includes an object with the id: category string key:value pairs with the boolean 'success'
- Sample: `curl http://127.0.0.1:5000/categories`

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
  "success": true
}
```

---

#### GET '/questions?page=${integer}'

- Retrieves a paginated list of questions, and the total number of questions, all categories, and the current category string.
- Request Arguments: integer 'page'
- Returns: An object containing a list of ten paginated questions, the total number of questions, an object containing all categories, the current category string, and the boolean 'success'.
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

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
  "current_category": "All", 
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
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```

---

#### GET '/categories/${id}/questions'

- Retrieves questions for a cateogry given by the id request parameter.
- Request Arguments: integer 'id'
- Returns: An object containing questions for the provided category, the total number of questions, the current category string, and the boolean 'success'.
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```json
{
  "current_category": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```

---
#### GET '/quizzes'

- Issues a post request to obtain the next question.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{ "previous_questions": [1, 4], "quiz_category": {"id": 1, "type": "Science"}}'`

- Request Body:

```json
{ 
    "previous_questions": [1, 4], 
    "quiz_category": {"id": 1, "type": "Science"}
}
```

- Returns a single new question object and the boolean 'success'.

```json
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```

---
#### POST '/questions'`

- Submits a post request to add a new question to the database.
- Sample: `curl -X POST http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "What is my name?", "answer": "John Adex", "difficulty": 1, "category": 1}'`

- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: 'success' boolean
```json
{
  "success": true
}
```

---

#### POST '/questions'

- Sends a post request to find a specific question using a search keyword.
- Sample: `curl -X POST -H "Content-Type: application/json" -d'{"searchTerm":"title"}' http://127.0.0.1:5000/questions`
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, and total number of questions that met the search phrase, current category string, and 'success' boolean.

```json
{
  "current_category": "All",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
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
  "total_questions": 20
}
```

---
#### DELETE '/questions/${id}'

- Using the question's id, deletes a specific question.
- Request Arguments: integer 'id'
- Returns: An integer with the id 'deleted' and the boolean 'success'.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`

```json
{
  "deleted": 10,
  "success": true
}
```

---


## Deployment N/A

## Authors
Thanks, Yours Truly, Adex, John.

## Acknowledgements 
The Udacity crew and all of the students, who will soon be full stack superstars!
