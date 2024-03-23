from flask_restful import Resource
from database import Database
from flask import request

database = Database()


class Cost(Resource):
    def post(self):
        data = request.get_json()
        res = database.add_cost(
            data["project_id"],
            data["name"],
            data["cost"],
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
            data["remark"],
            data["status"],
        )
        if response:
            return {"response": response}
