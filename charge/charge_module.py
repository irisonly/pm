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
        if database.add_charge(
            data["name"], data["level"], data["salary"], data["month"]
        ):
            return {"response": f"successful add charger {data['name']}"}
        return {"response": f"fail to add charger"}

    @jwt_required()
    def get(self):
        _id = request.args.get("id")
        data = database.get_charge(_id)
        if data is not None:
            return {"response": data}
        return {"response": "no such charger"}

    def delete(self):
        _id = int(request.args.get("id"))
        if database.delete_charge(_id):
            return {"response": f"successful delete charger {_id}"}
        return {"response": f"fail to delete charger"}

    def put(self):
        _id = int(request.args.get("id"))
        data = request.get_json()
        res = database.modify_charge(
            _id, data["name"], data["level"], data["salary"], data["month"]
        )
        if res:
            return {"response": "successful modify the charger"}
        return {"response": "fail to modify the charger"}
