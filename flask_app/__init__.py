import os, git, hmac, hashlib

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
    return 'test', 200


def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


@app.route('/update_back', methods=['POST'])
def mai_back_update():
    if request.method == 'POST':
        x_hub_signature = request.headers.get('X-Hub-Signature')
        secret_key = os.getenv('SECRET_KEY')
        check_valid = is_valid_signature(x_hub_signature, request.data, secret_key)
        if check_valid:
            repo = git.Repo('/home/mastaBlastaIT/mai_back/')
            origin = repo.remotes.origin
            origin.fetch()
            repo.merge_base(repo.heads.master, origin.refs.master)
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Invalid signature', 401
    else:
        return 'Wrong event type', 400


import flask_app.set_table
import flask_app.regexp
