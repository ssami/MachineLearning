"""
Redis: ~/Git_personal/MachineLearning/gutenberg/redis-stable/src/redis-server
Minio: [start Docker] docker run -p 9000:9000 -e "MINIO_ACCESS_KEY=admin" -e "MINIO_SECRET_KEY=password" minio/minio server /data
"""



from flask import Flask, request, jsonify
from src.db import get_db
from src import constants
from src.model import ModelInfo
from src.exceptions import InvalidDataError
from src.utils import allowed_files
from src.model import get_model
from flask import g

import os

app = Flask(__name__, instance_relative_config=True)
conn = get_db('RedisDB')
# db.init_app(app)
#TODO: fix app init
#  turned this off because "in do_teardown_appcontext
#  TypeError: close_db() takes 0 positional arguments but 1 was given""


@app.route("/")
def main():
    return "Hello, world!"


@app.route("/model", methods=["PUT", "GET"])
def all_models():
    if request.method == "GET":
        resp = [x for x in conn.findall(constants.MODEL_KEYSPACE)]
        return jsonify(resp), 200
    else:
        if request.is_json:
            data = request.get_json()
            model_info = ModelInfo(data['description'], data['metrics'], data['location'])
            try:
                # todo: fix how we store a dict of metrics
                conn.store(model_info.hash, model_info.items)
            except Exception as e:
                return jsonify(str(e)), 500
            return jsonify(model_info.hash), 201
        else:
            return jsonify(InvalidDataError("request is not in JSON")), 500


@app.route("/model/<model_id>", methods=["PUT", "GET"])
def model(model_id):
    if request.method == "GET":
        info_dict = conn.find(model_id)
        return jsonify(info_dict)

    is_live = request.args.get('live', None)   # look for liveness check
    if is_live:
        info_dict = conn.find(model_id)
        info_dict['live'] = is_live
        conn.store(info_dict['hash'], info_dict)
        # todo: how to pass the model type here? needs to be from model info
        model = get_model('FastTextModel', info_dict['location'], 'MinioLoader')
        g.model = model.load()
        return jsonify(model_id), 204  # model was set live successfully
    return jsonify('No liveness value specified'), 204


if __name__ == "__main__":
    # make sure the instance path is present
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.run(debug=1)