from flask import request
from flask_restful import Resource
from common.parser_module import Parser
from database import Database

database = Database()


class ProjectStatus(Resource):
    def post(self):
        parser = Parser()
        data = parser.output()
        if database.add_status(data["name"]):
            return {"response": f"successful add status {data['name']}"}
        return {"response": f"fail to add status"}

    def get(self):
        name = request.args.get("name")
        if name is None:
            name = ""
        data = database.get_status(name)
        if data is not None:
            return {"response": data}
        return {"response": "no such charger"}

    def delete(self):
        parser = Parser()
        data = parser.output()
        if database.delete_status(data["name"]):
            return {"response": f"successful delete type {data['name']}"}
        return {"response": f"fail to delete type"}
