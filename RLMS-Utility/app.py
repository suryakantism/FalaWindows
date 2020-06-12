from flask import Flask, jsonify, request, send_from_directory, Response, send_file
from flask_cors import CORS

from modules import tfidf, utils

from os import system

import decimal

# from flask_pymongo import PyMongo

app = Flask(__name__)
# utils.load_db_data()

# == testing ==
CORS(app)

# == config ==
app.url_map.strict_slashes = False
# app.config['MONGO_DBNAME'] = server_secrets.mongo_db_name
# app.config['MONGO_URI'] = server_secrets.mongo_uri

# == routes ==


@app.route('/', methods=['GET'])
def test():
    return jsonify({"Response": "Test response"})


@app.route('/', methods=['POST'])
def post_test():
    data = request.get_json()
    return jsonify({"Data": data})


@app.route('/tfidf/update', methods=['POST'])
def tfidf_update():
    data = request.get_json()

    try:
        section = data["section"]
        question = data["question"]
        user_data = data["user_data"]

    except KeyError:
        return jsonify({"Error": "Incorrect query keys."})

    utils.add_db_data(section, question, user_data)

    return jsonify({"Message": "OK."})


@app.route('/tfidf/request', methods=['POST'])
def tfidf_request():
    print(request.get_json())

    try:
        data = request.get_json()
        section = data["section"]
        if section not in ["ari", "ccpa", "escrow", "gi", "heloc", "ii", "pdp", "pi", "pt", "rlt", "sm", "tax_statement"]:
            return jsonify({"Message": "DEVERROR: Section name not found."})

        else:
            response = tfidf.get_tfidf_response(data["user_input"], section)
            return jsonify(response)

    except Exception as e:
        return jsonify({"Message": str(e)})


@app.route('/tfidf/raw/<section>', methods=['GET'])
def tfidf_raw(section):
    try:
        print(section)
        data = utils.fetch_faq_data(section, raw=True)
        questions = data[0][1:]
        return jsonify({"data": questions})

    except Exception as e:
        return jsonify({"Message": str(e)})


@app.route('/canned/dynamic/request', methods=['POST'])
def canned_dynamic_request():
    data = request.get_json()

    loan_number = data["loan_number"]
    question_id = data["question_id"]

    response_strings = utils.build_dynamic_response(loan_number, question_id)

    return jsonify({"responses": response_strings})


if __name__ == '__main__':
    app.run(host='localhost', port=5005)
