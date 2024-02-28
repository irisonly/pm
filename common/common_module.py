from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from flask_restful import Resource
from flask import request
from database import Database

database = Database()


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        data = request.get_json()
        access_token = create_access_token(identity=get_jwt_identity())
        return {"response": {"access_token": access_token}}


def transfer_zero(arg):
    try:
        int(arg)
    except ValueError:
        return None
    else:
        return int(arg)


class DashBoard(Resource):
    @jwt_required()
    def get(self):
        return {"response": database.count_sum()}


class Excel(Resource):
    def get(self):
        return database.out_data()
