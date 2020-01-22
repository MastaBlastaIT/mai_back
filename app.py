import json, math

from flask import Flask, request, jsonify
from numpy.random import uniform
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/set_table": {"origins": "*"}}, methods=['POST'])
app.config["DEBUG"] = True


def generate_initials_list(count):
    return uniform(1.1, 59.9, count)


def nth_root_row(a, n, initial_guess):
    eps = 0.1
    x = initial_guess
    rows = [x]
    while True:
        delta_x = ((a / math.pow(x, n - 1)) - x) / n
        x += delta_x
        rows.append(x)
        if math.fabs(delta_x) < eps:
            break
    return rows


def convert_to_row(arr):
    row_dict = {}
    for i, x in enumerate(arr):
        prefix = i // 26
        prefix_letter = '' if prefix == 0 else chr(prefix + 64)
        row_dict[prefix_letter + chr((i % 26) + 65)] = x
    return row_dict


def convert_to_chart(arr):
    return {i: x for i, x in enumerate(arr)}


@app.route('/', methods=['GET'])
def home():
    return '', 404


@app.route('/set_table', methods=['POST'])
def set_table():
    errors_dict = {'errors': []}
    cols_count = 0
    variable = 0.0
    exponent = 0
    initials_array = []

    try:
        cols_count = int(request.form['cols_count'])
    except ValueError:
        errors_dict['errors'].append({
            'cols_count': 'is not integer',
        })

    try:
        variable = float(request.form['variable'])
    except ValueError:
        errors_dict['errors'].append({
            'variable': 'is not number',
        })

    try:
        exponent = int(request.form['exponent'])
    except ValueError:
        errors_dict['errors'].append({
            'exponent': 'is not integer',
        })

    try:
        initials_array_field = request.form.get('initials_array', '[]')
        initials_array = json.loads(initials_array_field)
        if type(initials_array) is not list:
            raise TypeError
    except (json.decoder.JSONDecodeError, TypeError):
        errors_dict['errors'].append({
            'initials_array': 'is not list',
        })

    if len(errors_dict['errors']) > 0:
        return jsonify(errors_dict), 400

    if len(initials_array) <= 0:
        initials_array = generate_initials_list(cols_count)
    elif len(initials_array) < cols_count:
        additional_array = list(generate_initials_list(cols_count - len(initials_array)))
        initials_array += additional_array
    else:
        initials_array = initials_array[:cols_count]
    cols_arr = []

    for guess in initials_array:
        col = nth_root_row(variable, exponent, guess)
        cols_arr.append(col)

    rows_count = max([len(x) for x in cols_arr])
    rows_arr = []
    for i in range(rows_count):
        row = convert_to_row([cols_arr[j][i] if i < len(cols_arr[j]) else None for j in range(cols_count)])
        rows_arr.append(row)

    charts_arr = []
    for arr in cols_arr:
        charts_arr.append(convert_to_chart(arr))

    return jsonify({
        'table_rows': rows_arr,
        'rows_count': rows_count,
        'charts': charts_arr,
    }), 200


app.run()
