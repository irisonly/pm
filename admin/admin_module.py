from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash
from database import Database
from flask_jwt_extended import jwt_required

database = Database()


class Admin(Resource):
    def post(self):
        data = request.get_json()
        user_name = data["user_name"]
        password = data["password"]
        password_hash = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=8
        )
        if database.add_administrator(user_name, password_hash):
            return {"response": f"successful add admin {data['user_name']}"}
        return {"response": f"fail to add admin"}

    @jwt_required()
    def get(self):
        data = database.get_administrator()
        if data:
            return {"response": data}
        return {"response": "no admin"}


class AdminProject(Resource):
    def post(self):
        data = request.get_json()
        admin_id = data["admin_id"]
        project_list = data["project_list"]
        response = database.add_admin_projects(project_list, admin_id)
        if response:
            return {"response": f"successful add admin projects{response}"}
        return {"response": f"fail to add admin projects"}

    def get(self):
        admin_id = request.args.get("id")
        response = database.get_admin_projects(admin_id, "checked")
        if response:
            return {"response": response}
        return {"response": []}
