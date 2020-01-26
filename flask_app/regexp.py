import re

from flask_app import app, mysql
from flask import request, jsonify
from flask_cors import CORS

cors = CORS(app, resources={r"/regexp_find": {"origins": "*"}}, methods=['POST'])


def get_flag_value(f):
    if f == 'i':
        return re.IGNORECASE
    if f == 'm':
        return re.MULTILINE
    if f == 's':
        return re.DOTALL
    if f == 'u':
        return re.UNICODE
    return 0


def get_flags(flags_str):
    flags_sum = 0
    for f in flags_str:
        flags_sum |= get_flag_value(f)
    return flags_sum


@app.route('/regexp_find', methods=['POST'])
def regexp_find():
    errors_dict = {'errors': []}
    text_type = 1
    try:
        text_type = int(request.form.get('text_type'))
    except TypeError:
        errors_dict['errors'].append({
            'text_type': 'is not integer or empty field',
        })

    if len(errors_dict['errors']) > 0:
        return jsonify(errors_dict), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT text_field FROM texts_table where id = '%s'" % text_type)
    initial_text = cur.fetchone()[0]
    res_obj = {'initial_text': initial_text}
    cur.close()

    regex_str = request.form.get('regex_str')
    if regex_str:
        regex = regex_str[1:].split('/')
        regexp_test = re.finditer(r'%s' % regex[0], r'%s' % initial_text, flags=get_flags(regex[1]))
        res_str = ''
        pos = 0
        for x in regexp_test:
            res_str += initial_text[pos:x.start()] + ('<span>%s<span>' % x[0])
            pos = x.start() + len(x[0])
            print(x[0], x.start())
        res_str += initial_text[pos:]
        res_obj['regexp_found'] = res_str
    return jsonify(res_obj), 200
