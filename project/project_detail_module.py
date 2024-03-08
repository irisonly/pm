from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from database import Database
from common.parser_module import ProjectParser
from flask import request
from common.common_module import transfer_zero

database = Database()


class ProjectDetail(Resource):
    # @jwt_required()
    def post(self):
        parser = ProjectParser()
        data = parser.output()
        if database.add_project(
            data["name"],
            data["start_time"],
            data["end_time"],
            data["type_id"],
            data["m_id_list"],
            data["p_id_list"],
            data["status_id"],
            data["payment"],
            data["balance_payment"],
        ):
            return {"response": f"successful add project {data['name']}"}
        return {"response": f"fail to add project"}

    @jwt_required()
    def get(self):
        query = database.get_project(
            name=None if request.args.get("name") == "" else request.args.get("name"),
            _id=transfer_zero(request.args.get("id")),
            charge_m_id=transfer_zero(request.args.get("charge_m_id")),
            charge_p_id=transfer_zero(request.args.get("charge_p_id")),
            type_id=transfer_zero(request.args.get("type_id")),
        )

        if query is not None:
            return {"response": query}
        return {"response": "no such project"}

    def put(self):
        parser = ProjectParser()
        data = parser.output()
        if database.update_project(
            data["id"],
            data["name"],
            data["start_time"],
            data["end_time"],
            data["type_id"],
            data["m_id_list"],
            data["p_id_list"],
            data["status_id"],
            data["payment"],
            data["balance_payment"],
        ):
            return {"response": f"successful update project {data['name']}"}
        return {"response": f"fail to update project"}

    def delete(self):
        _id = request.get_json()["id"]
        if database.delete_project(_id):
            return {"response": f"successful delete delete the project"}
        return {"response": f"fail to delete the project"}
