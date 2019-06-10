# Quizizz

This project is made as a part of assignment for the backend intern position at Quizizz.

### Steps to run server -

Step-1 : Create virtual Environment - [Resource](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Step-2 : Clone this repo.
```
$ git clone https://github.com/techytoes/Quizizz.git
$ cd Quizizz
```

Step-3 : Install python libraries and packages.
```
$ pip install -r requirements.txt
```
Step-4 : Run Django Server.
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```

The Server will start on http://127.0.0.1:8000/

## API -

|    Functions    |                      URLs                      |                                    Request                                    |             Response             |
|:---------------:|:----------------------------------------------:|:-----------------------------------------------------------------------------:|:--------------------------------:|
|  Register User  |   http://127.0.0.1:8000/api/v3/user/register/  |           name, date_of_birth, occupation, email, username, password          |      Registration Successful     |
|    Login User   |    http://127.0.0.1:8000/api/v3/user/login/    |                               username, password                              |      Dashboard for the user      |
|   Add Question  |   http://127.0.0.1:8000/api/v3/question/add/   | username, password,  question_body, options(list of int), correct option(int) |    Question added successfully   |
|     Add Quiz    |     http://127.0.0.1:8000/api/v3/quiz/add/     |                               username, password                              |      Quiz added Successfully     |
|   Create Game   |    http://127.0.0.1:8000/api/v3/create/game/   |                       username, password, allowed_users(list of names)                       |     Game created Successfully    |
|    Play Game    |     http://127.0.0.1:8000/api/v3/play/game/    |                         username, password, created_by                        |      Display Game Questions      |
| Submit Response | http://127.0.0.1:8000/api/v3/play/game/submit/ |                   username, password, created_by, responses                   | Responses submitted successfully |
|   Leaderboard   |    http://127.0.0.1:8000/api/v3/leaderboard/   |                               username, password                              |            Leaderboard           |
