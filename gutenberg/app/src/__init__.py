from flask import Flask, request, jsonify
from .db import get_db
from .constants import MODEL_KEYSPACE
from .model import ModelInfo
from .exceptions import InvalidDataError

app = Flask(__name__)
conn = get_db()
# db.init_app(app)
#TODO: fix app init
#  turned this off because "in do_teardown_appcontext
#  TypeError: close_db() takes 0 positional arguments but 1 was given""


@app.route("/")
def main():
    return "Hello, world!"


@app.route("/model", methods=("POST", "GET"))
def model():
    if request.method == "GET":
        model_list = [x.decode('utf-8') for x in conn.smembers(MODEL_KEYSPACE)]
        return jsonify(model_list), 200
    else:
        if request.is_json:
            data = request.get_json()
            model_info = ModelInfo(data['description'], data['metrics'])
            try:
                conn.sadd(MODEL_KEYSPACE, model_info.hash)
                print(model_info.items())
                conn.hmset(model_info.hash, model_info.items())
            except Exception as e:
                return jsonify(str(e)), 500
            return jsonify("Success"), 201
        else:
            return jsonify(InvalidDataError("request is not in JSON")), 500

