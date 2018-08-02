from flask import Flask, request, jsonify
from .db import *

app = Flask(__name__)
conn = db.get_db()
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
        model_list = [x.decode('utf-8') for x in conn.smembers('models')]
        return jsonify(model_list)
