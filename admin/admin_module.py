from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash
from database import Database

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

    def get(self):
        data = database.get_administrator()
        if data:
            return {"response": data}
        return {"response": "no admin"}
