# Quizizz

Steps to run server -

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