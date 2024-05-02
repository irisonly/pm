from flask_restful import Resource
from database import Database
from flask import request
from flask_jwt_extended import jwt_required

database = Database()


class Invoice(Resource):
    def post(self):
        data = request.get_json()
        res = database.add_invoice(
            data["project_id"],
            data["name"],
            data["invoice"],
            data["month"],
            data["remark"],
        )
        if res:
            return {"response": res}

    def get(self):
        _id = request.args.get("id")
        print(_id)
        if request.args.get("c_id"):
            res = database.get_single_invoice(request.args.get("c_id"))
        else:
            res = database.get_invoice(_id)
        if res:
            return {"response": res}

    def delete(self):
        _id = request.get_json()["id"]
        print(_id)
        res = database.delete_invoice(_id)
        if res:
            return {"response": f"successful delete the cost"}
        return {"response": f"fail to delete the cost"}

    # TODO
    def put(self):
        data = request.get_json()
        response = database.modify_invoice(
            data["id"],
            data["name"],
            data["invoice"],
            data["month"],
            data["remark"],
        )
        if response:
            return {"response": response}
        return {"response": f"fail to modify the invoice"}
