from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from werkzeug.security import check_password_hash
from flask_restful import Resource
from flask import request
from database import Database

database = Database()


class Login(Resource):
    def post(self):
        data = request.get_json()
        user_name = data["user_name"]
        password = data["password"]
        admin_mapping = database.administrator_mapping()
        print("admin_mapping")
        if user_name in admin_mapping and check_password_hash(
            admin_mapping[user_name]["password"], password
        ):
            if admin_mapping[user_name]["id"] == 1:
                additional_claims = {"role": "admin"}
            else:
                additional_claims = {"role": "user"}
            access_token = create_access_token(
                admin_mapping[user_name]["id"], additional_claims=additional_claims
            )
            refresh_token = create_refresh_token(admin_mapping[user_name]["id"])
            return {
                "response": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            }
        return {"response": "error"}
