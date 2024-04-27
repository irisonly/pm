from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from common.parser_module import Parser
from database import Database

database = Database()


class ProjectType(Resource):
    def post(self):
        parser = Parser()
        data = parser.output()
        if database.add_type(data["name"]):
            return {"response": f"successful add type {data['name']}"}
        return {"response": f"fail to add type"}

    @jwt_required()
    def get(self):
        name = request.args.get("name")
        if name is None:
            name = ""
        data = database.get_type(name)
        if data is not None:
            return {"response": data}
        return {"response": "no such type"}

    def delete(self):
        parser = Parser()
        data = parser.output()
        if database.delete_type(data["name"]):
            return {"response": f"successful delete type {data['name']}"}
        return {"response": f"fail to delete type"}
