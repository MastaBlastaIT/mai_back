import git

from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL pythonanywhere configurations
app.config['MYSQL_USER'] = 'mastaBlastaIT'
app.config['MYSQL_PASSWORD'] = '9@RYKQTWHtw38qP'
app.config['MYSQL_DB'] = 'mastaBlastaIT$regexp_texts'
app.config['MYSQL_HOST'] = 'mastaBlastaIT.mysql.pythonanywhere-services.com'

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def home():
    return '', 404


@app.route('/update_back', methods=['POST'])
def mai_back_update():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/MastaBlastaIT/mai_back.git')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


import flask_app.set_table
import flask_app.regexp
