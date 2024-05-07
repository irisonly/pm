from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from database import Database
from flask_cors import CORS
from datetime import timedelta
from admin.admin_module import Admin, AdminProject
from login.login_module import Login
from common.common_module import DashBoard, Excel, Import
from charge.charge_module import Charge
from project.project_type_module import ProjectType
from project.project_status_module import ProjectStatus
from project.project_list_module import ProjectList
from project.project_detail_module import ProjectDetail
from cost.cost_module import Cost, CostOverall
from level.level_module import Level
from invoice.invoice_module import Invoice, InvoiceOverall


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
api.add_resource(AdminProject, "/adminproject")
api.add_resource(CostOverall, "/costoverall")
api.add_resource(Invoice, "/invoice")
api.add_resource(InvoiceOverall, "/invoiceoverall")

if __name__ == "__main__":
    app.run(port=4000, debug=True)  # 启动 Flask 应用，监听 4000 端口
