from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt
from database import Database

database = Database()


class ProjectList(Resource):
    @jwt_required()
    def get(self):
        admin_id = request.args.get("id")

        data = database.get_project_list(admin_id)
        if data is not None:
            return {"response": data}
        return {"response": "no more project"}
