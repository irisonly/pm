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
