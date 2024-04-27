from flask_restful import Resource
from database import Database
from flask import request
from flask_jwt_extended import jwt_required

database = Database()


class Cost(Resource):
    def post(self):
        data = request.get_json()
        res = database.add_cost(
            data["project_id"],
            data["name"],
            data["cost"],
            data["month"],
            data["remark"],
            data["status"],
        )
        if res:
            return {"response": res}

    def get(self):
        _id = request.args.get("id")
        if request.args.get("c_id"):
            res = database.get_single_cost(request.args.get("c_id"))
        else:
            res = database.get_cost(_id)
        if res:
            return {"response": res}

    def delete(self):
        _id = request.get_json()["pid"]
        data = request.get_json()["id"]
        print(_id, data)
        res = database.delete_cost(data, _id)
        if res:
            return {"response": f"successful delete the cost"}
        return {"response": f"fail to delete the cost"}

    def put(self):
        data = request.get_json()
        response = database.modify_cost(
            data["id"],
            data["name"],
            data["cost"],
            data["month"],
            data["remark"],
            data["status"],
        )
        if response:
            return {"response": response}


class CostOverall(Resource):
    @jwt_required()
    def get(self):
        month = int(request.args.get("month"))
        print(month)
        response = database.get_cost_overall(month)
        if response:
            return {"response": response}
