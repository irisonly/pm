from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request
from common.parser_module import Parser
from database import Database

database = Database()


class Charge(Resource):
    def post(self):
        parser = Parser()
        data = parser.output()
        if database.add_charge(data["name"], data["level"], data["salary"]):
            return {"response": f"successful add charger {data['name']}"}
        return {"response": f"fail to add charger"}

    @jwt_required()
    def get(self):
        name = request.args.get("name")
        data = database.get_charge(name)
        if data is not None:
            return {"response": data}
        return {"response": "no such charger"}

    def delete(self):
        name = request.args.get("name")
        if database.delete_charge(name):
            return {"response": f"successful delete charger {name}"}
        return {"response": f"fail to delete charger"}

    def put(self):
        _id = request.args.get("name")
        data = request.get_json()
        res = database.modify_charge(data["name"], data["level"], data["salary"])
        if res:
            return {"response": "successful modify the charger"}
        return {"response": "fail to modify the charger"}
