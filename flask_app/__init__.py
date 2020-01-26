from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL localhost configurations
app.config['MYSQL_USER'] = 'regexp_user'
app.config['MYSQL_PASSWORD'] = 'fRXsW7A9'
app.config['MYSQL_DB'] = 'regexp_texts'
app.config['MYSQL_HOST'] = 'localhost'

# MySQL pythonanywhere configurations
# app.config['MYSQL_USER'] = 'mastaBlastaIT'
# app.config['MYSQL_PASSWORD'] = '9@RYKQTWHtw38qP'
# app.config['MYSQL_DB'] = 'mastaBlastaIT$regexp_texts'
# app.config['MYSQL_HOST'] = 'mastaBlastaIT.mysql.pythonanywhere-services.com'

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def home():
    return '', 404


import flask_app.set_table
import flask_app.regexp
