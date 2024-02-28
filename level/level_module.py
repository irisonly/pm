from flask import request
from database import Database
from flask_restful import Resource

database = Database()


class Level(Resource):
    def post(self):
        data = request.get_json()
        res = database.add_level(data["name"])
        if res:
            return {"response": res}

    def get(self):
        res = database.get_level()
        if res:
            return {"response": res}
