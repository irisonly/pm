from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from database import Database
from flask_cors import CORS
from datetime import timedelta
from admin.admin_module import Admin
from login.login_module import Login
from common.common_module import DashBoard, Excel, Import
from charge.charge_module import Charge
from project.project_type_module import ProjectType
from project.project_status_module import ProjectStatus
from project.project_list_module import ProjectList
from project.project_detail_module import ProjectDetail
from cost.cost_module import Cost
from level.level_module import Level


app = Flask(__name__)  # 创建 Flask 应用实例
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///database.db"  # 配置数据库 URI，这里使用的是 SQLite
)
app.config["SECRET_KEY"] = "secret_token"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
api = Api(app)  # 创建 Flask-REST API 实例
database = Database()  # 创建数据库实例
database.db.init_app(app)  # 初始化数据库与 Flask 应用的关联
CORS(app)
jwt = JWTManager(app)


with app.app_context():  # 在应用上下文中
    database.create_table()  # 创建数据库表


@app.route("/")
def home():
    return "API engine has launched"


api.add_resource(Charge, "/charge")  # 将 Charge 资源注册
api.add_resource(ProjectType, "/type")  # 将 ProjectType 资源注册到 /type 路径
api.add_resource(ProjectStatus, "/status")  # 将 ProjectStatus 资源注册到 /status 路径
api.add_resource(ProjectList, "/projectlist")
api.add_resource(ProjectDetail, "/project")
api.add_resource(DashBoard, "/dashboard")
api.add_resource(Admin, "/admin")
api.add_resource(Login, "/login")
api.add_resource(Excel, "/excel")
api.add_resource(Cost, "/cost")
api.add_resource(Level, "/level")
api.add_resource(Import, "/import")

if __name__ == "__main__":
    app.run(port=4000, debug=True)  # 启动 Flask 应用，监听 4000 端口


# def transfer_zero(arg):
#     try:
#         int(arg)
#     except ValueError:
#         return None
#     else:
#         return int(arg)
#
# class Admin(Resource):
#     def post(self):
#         data = request.get_json()
#         user_name = data["user_name"]
#         password = data["password"]
#         password_hash = generate_password_hash(
#             password, method="pbkdf2:sha256", salt_length=8
#         )
#         if database.add_administrator(user_name, password_hash):
#             return {"response": f"successful add admin {data['user_name']}"}
#         return {"response": f"fail to add admin"}
#
#     def get(self):
#         data = database.get_administrator()
#         if data:
#             return {"response": data}
#         return {"response": "no admin"}
#
# class Login(Resource):
#     def post(self):
#         data = request.get_json()
#         user_name = data["user_name"]
#         password = data["password"]
#         admin_mapping = database.administrator_mapping()
#         print("admin_mapping")
#         if user_name in admin_mapping and check_password_hash(
#             admin_mapping[user_name]["password"], password
#         ):
#             if admin_mapping[user_name]["id"] == 1:
#                 additional_claims = {"role": "admin"}
#             else:
#                 additional_claims = {"role": "user"}
#             access_token = create_access_token(
#                 admin_mapping[user_name]["id"], additional_claims=additional_claims
#             )
#             refresh_token = create_refresh_token(admin_mapping[user_name]["id"])
#             return {
#                 "response": {
#                     "access_token": access_token,
#                     "refresh_token": refresh_token,
#                 }
#             }
#         return {"response": "error"}
#
# class Refresh(Resource):
#     @jwt_required(refresh=True)
#     def post(self):
#         data = request.get_json()
#         access_token = create_access_token(identity=get_jwt_identity())
#         return {"response": {"access_token": access_token}}
#
# class Parser:
#     def __init__(self):
#         self.parser = reqparse.RequestParser()  # 创建请求解析器
#         self.parser.add_argument("name", type=str, required=True)  # 添加请求参数
#         self.parser.add_argument("id", type=int, required=False)
#         self.parser.add_argument("level", type=int, required=False)
#         self.parser.add_argument("salary", type=float, required=False)
#
#     def output(self):
#         return self.parser.parse_args()  # 解析并返回请求参数
#
#
# class ProjectParser:
#     def __init__(self):
#         self.parser = reqparse.RequestParser()  # 创建请求解析器
#         self.parser.add_argument("id", type=int, required=False)  # 添加请求参数
#         self.parser.add_argument("name", type=str, required=True)  # 添加请求参数
#         self.parser.add_argument("start_time", type=str, required=True)
#         self.parser.add_argument("end_time", type=str, required=True)
#         self.parser.add_argument("type_id", type=int, required=True)
#         self.parser.add_argument("m_id_list", type=int, action="append", required=False)
#         self.parser.add_argument("p_id_list", type=int, action="append", required=False)
#         self.parser.add_argument("status_id", type=int, required=True)
#         self.parser.add_argument("payment", type=float, required=True)
#         self.parser.add_argument("cost", type=float, required=False)
#         self.parser.add_argument("balance_payment", type=float, required=True)
#
#     def output(self):
#         return self.parser.parse_args()  # 解析并返回请求参数
#
# class Charge(Resource):
#     def post(self):
#         parser = Parser()
#         data = parser.output()
#         if database.add_charge(data["name"], data["level"], data["salary"]):
#             return {"response": f"successful add charger {data['name']}"}
#         return {"response": f"fail to add charger"}
#
#     @jwt_required()
#     def get(self):
#         name = request.args.get("name")
#         data = database.get_charge(name)
#         if data is not None:
#             return {"response": data}
#         return {"response": "no such charger"}
#
#     def delete(self):
#         name = request.args.get("name")
#         if database.delete_charge(name):
#             return {"response": f"successful delete charger {name}"}
#         return {"response": f"fail to delete charger"}
#
#     def put(self):
#         _id = request.args.get("name")
#         data = request.get_json()
#         res = database.modify_charge(data["name"], data["level"], data["salary"])
#         if res:
#             return {"response": "successful modify the charger"}
#         return {"response": "fail to modify the charger"}
#
# class ProjectType(Resource):
#     def post(self):
#         parser = Parser()
#         data = parser.output()
#         if database.add_type(data["name"]):
#             return {"response": f"successful add type {data['name']}"}
#         return {"response": f"fail to add type"}
#
#     @jwt_required()
#     def get(self):
#         name = request.args.get("name")
#         data = database.get_type(name)
#         if data is not None:
#             return {"response": data}
#         return {"response": "no such type"}
#
#     def delete(self):
#         parser = Parser()
#         data = parser.output()
#         if database.delete_type(data["name"]):
#             return {"response": f"successful delete type {data['name']}"}
#         return {"response": f"fail to delete type"}
#
# class ProjectStatus(Resource):
#     def post(self):
#         parser = Parser()
#         data = parser.output()
#         if database.add_status(data["name"]):
#             return {"response": f"successful add status {data['name']}"}
#         return {"response": f"fail to add status"}
#
#     def get(self):
#         name = request.args.get("name")
#         data = database.get_status(name)
#         if data is not None:
#             return {"response": data}
#         return {"response": "no such charger"}
#
#     def delete(self):
#         parser = Parser()
#         data = parser.output()
#         if database.delete_status(data["name"]):
#             return {"response": f"successful delete type {data['name']}"}
#         return {"response": f"fail to delete type"}
#
# class ProjectList(Resource):
#     @jwt_required()
#     def get(self):
#         claims = get_jwt()
#         print(claims)
#         data = database.get_project_list()
#         if data is not None:
#             return {"response": data}
#         return {"response": "no more project"}
#
# class ProjectDetail(Resource):
#     # @jwt_required()
#     def post(self):
#         parser = ProjectParser()
#         data = parser.output()
#         if database.add_project(
#             data["name"],
#             data["start_time"],
#             data["end_time"],
#             data["type_id"],
#             data["m_id_list"],
#             data["p_id_list"],
#             data["status_id"],
#             data["payment"],
#             data["balance_payment"],
#         ):
#             return {"response": f"successful add project {data['name']}"}
#         return {"response": f"fail to add project"}
#
#     @jwt_required()
#     def get(self):
#         query = database.get_project(
#             name=None if request.args.get("name") == "" else request.args.get("name"),
#             _id=transfer_zero(request.args.get("id")),
#             charge_m_id=transfer_zero(request.args.get("charge_m_id")),
#             charge_p_id=transfer_zero(request.args.get("charge_p_id")),
#             type_id=transfer_zero(request.args.get("type_id")),
#         )
#         if query is not None:
#             return {"response": query}
#         return {"response": "no such project"}
#
#     def put(self):
#         parser = ProjectParser()
#         data = parser.output()
#         if database.update_project(
#             data["id"],
#             data["name"],
#             data["start_time"],
#             data["end_time"],
#             data["type_id"],
#             data["m_id_list"],
#             data["p_id_list"],
#             data["status_id"],
#             data["payment"],
#             data["balance_payment"],
#         ):
#             return {"response": f"successful update project {data['name']}"}
#         return {"response": f"fail to update project"}
#
#     def delete(self):
#         _id = request.get_json()["id"]
#         if database.delete_project(_id):
#             return {"response": f"successful delete delete the project"}
#         return {"response": f"fail to delete the project"}
#
# class DashBoard(Resource):
#     @jwt_required()
#     def get(self):
#         return {"response": database.count_sum()}
#
# class Excel(Resource):
#     def get(self):
#         return database.out_data()
#
# class Cost(Resource):
#     def post(self):
#         data = request.get_json()
#         res = database.add_cost(
#             data["name"], data["project_id"], data["name"], data["cost"], data["remark"]
#         )
#         if res:
#             return {"response": res}
#
#     def get(self):
#         _id = request.args.get("id")
#         res = database.get_cost(_id)
#         if res:
#             return {"response": res}
#
#     def delete(self):
#         data = request.get_json()["id"]
#         res = database.delete_cost(data)
#         if res:
#             return {"response": f"successful delete the cost"}
#         return {"response": f"fail to delete the cost"}
#
# class Level(Resource):
#     def post(self):
#         data = request.get_json()
#         res = database.add_level(data["name"])
#         if res:
#             return {"response": res}
#
#     def get(self):
#         res = database.get_level()
#         if res:
#             return {"response": res}
