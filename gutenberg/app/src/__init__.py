from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from src.db import get_db
from src import constants
from src.model import ModelInfo
from src.exceptions import InvalidDataError
from src.utils import allowed_files

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


@app.route("/model", methods=["POST", "GET"])
def model():
    if request.method == "GET":
        model_list = [x.decode('utf-8') for x in conn.find(constants.MODEL_KEYSPACE)]
        return jsonify(model_list), 200
    else:
        if request.is_json:
            data = request.get_json()
            model_info = ModelInfo(data['description'], data['metrics'], None)
            try:
                conn.store(constants.MODEL_KEYSPACE, model_info.hash)
                conn.store(model_info.hash, model_info.items)
            except Exception as e:
                return jsonify(str(e)), 500
            return jsonify("Success"), 201
        else:
            return jsonify(InvalidDataError("request is not in JSON")), 500


@app.route("/model_upload", methods=["POST", "GET"])
def model_upload():
    app.config['UPLOAD_CONSTANTS'] = constants.UPLOADS_FOLDER
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        fl = request.files['file']
        if fl and allowed_files(fl.filename, constants.ALLOWED_EXTENSIONS):
            filename = secure_filename(fl.filename)
            try:
                fl.save(os.path.join(app.instance_path, filename))
                return jsonify("File successfully uploaded!"), 200
            except Exception as e:
                return jsonify(str(e)), 500
        return 'No file or unaccepted format', 400

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    # make sure the instance path is present
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.run(debug=1)