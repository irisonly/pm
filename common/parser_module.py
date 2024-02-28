from flask_restful import reqparse


class Parser:
    def __init__(self):
        self.parser = reqparse.RequestParser()  # 创建请求解析器
        self.parser.add_argument("name", type=str, required=True)  # 添加请求参数
        self.parser.add_argument("id", type=int, required=False)
        self.parser.add_argument("level", type=int, required=False)
        self.parser.add_argument("salary", type=float, required=False)

    def output(self):
        return self.parser.parse_args()  # 解析并返回请求参数


class ProjectParser:
    def __init__(self):
        self.parser = reqparse.RequestParser()  # 创建请求解析器
        self.parser.add_argument("id", type=int, required=False)  # 添加请求参数
        self.parser.add_argument("name", type=str, required=True)  # 添加请求参数
        self.parser.add_argument("start_time", type=str, required=True)
        self.parser.add_argument("end_time", type=str, required=True)
        self.parser.add_argument("type_id", type=int, required=True)
        self.parser.add_argument("m_id_list", type=int, action="append", required=False)
        self.parser.add_argument("p_id_list", type=int, action="append", required=False)
        self.parser.add_argument("status_id", type=int, required=True)
        self.parser.add_argument("payment", type=float, required=True)
        self.parser.add_argument("cost", type=float, required=False)
        self.parser.add_argument("balance_payment", type=float, required=True)

    def output(self):
        return self.parser.parse_args()  # 解析并返回请求参数
