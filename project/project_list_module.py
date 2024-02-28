from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from database import Database

database = Database()


class ProjectList(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        print(claims)
        data = database.get_project_list()
        if data is not None:
            return {"response": data}
        return {"response": "no more project"}
