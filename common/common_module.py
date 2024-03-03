from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from flask_restful import Resource
from flask import request
from database import Database
from werkzeug.utils import secure_filename
import os

database = Database()
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def transfer_zero(arg):
    try:
        int(arg)
    except ValueError:
        return None
    else:
        return int(arg)


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        data = request.get_json()
        access_token = create_access_token(identity=get_jwt_identity())
        return {"response": {"access_token": access_token}}


class DashBoard(Resource):
    @jwt_required()
    def get(self):
        return {"response": database.count_sum()}


class Excel(Resource):
    def get(self):
        return database.out_data()


class Import(Resource):
    def post(self):
        _id = request.args.get("id")

        if "file" not in request.files:
            return {"msg": "not file"}
        file = request.files["file"]
        if file.filename == "":
            return {"msg": "no file name"}
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            database.read_file(filepath, _id)
