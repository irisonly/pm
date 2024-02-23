from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Integer,
    Float,
    String,
    ForeignKey,
    exc,
    and_,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
)
from flask import send_file
import pandas


class Base(DeclarativeBase):
    pass


# TODO
db = SQLAlchemy(model_class=Base)

project_charge_association = db.Table(
    "project_charge_link",
    db.Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    db.Column(
        "p_charge_id", Integer, ForeignKey("project_charge.id"), primary_key=True
    ),
)
# TODO
project_charge_association_m = db.Table(
    "project_charge_link_m",
    db.Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    db.Column(
        "m_charge_id", Integer, ForeignKey("project_charge.id"), primary_key=True
    ),
)


class Admin(db.Model):
    __tablename__ = "admin"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    user_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)


class ProjectType(db.Model):
    __tablename__ = "project_type"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    related_project = relationship("Project", backref="type_name")


# TODO
class ProjectCharge(db.Model):
    __tablename__ = "project_charge"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    level: Mapped[int] = mapped_column(Integer, ForeignKey("level.id"), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    m_projects = relationship(
        "Project", secondary=project_charge_association_m, back_populates="m_charges"
    )
    p_projects = relationship(
        "Project", secondary=project_charge_association, back_populates="p_charges"
    )


class Level(db.Model):
    __tablename__ = "level"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    related_charge = relationship("ProjectCharge", backref="level_name")


class ProjectStatus(db.Model):
    __tablename__ = "project_status"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    related_project = relationship("Project", backref="status_name")


# TODO
class Project(db.Model):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project_type.id"), nullable=False
    )
    profit_rate: Mapped[float] = mapped_column(Float, nullable=False)
    payment: Mapped[float] = mapped_column(Float, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    tax: Mapped[float] = mapped_column(Float, nullable=False)
    balance_payment: Mapped[float] = mapped_column(Float, nullable=False)
    profit: Mapped[float] = mapped_column(Float, nullable=False)
    m_charges = relationship(
        "ProjectCharge",
        secondary=project_charge_association_m,
        back_populates="m_projects",
    )
    p_charges = relationship(
        "ProjectCharge",
        secondary=project_charge_association,
        back_populates="p_projects",
    )
    start_time: Mapped[str] = mapped_column(String, nullable=False)
    end_time: Mapped[str] = mapped_column(String, nullable=False)
    status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project_status.id"), nullable=False
    )
    project_cost = relationship("ProjectCost", backref="total_cost")


class ProjectCost(db.Model):
    __tablename__ = "project_cost"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    remark: Mapped[str] = mapped_column(String, nullable=True)


class Database:
    def __init__(self):
        self.db = db

    def create_table(self):
        self.db.create_all()

    def add_charge(self, name, level, salary):
        record = ProjectCharge(name=name, level=level, salary=salary)
        self.db.session.add(record)
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            return True

    def get_charge(self, name=None):
        if not name:
            records = (
                self.db.session.execute(
                    self.db.select(ProjectCharge).order_by(ProjectCharge.id)
                )
                .scalars()
                .all()
            )
            print(records)
            if records:
                records_output = [
                    {
                        "id": i.id,
                        "name": i.name,
                        "level": i.level_name.name,
                        "salary": i.salary,
                        "m_projects": [c.name for c in i.m_projects],
                        "p_projects": [c.name for c in i.p_projects],
                    }
                    for i in records
                ]
                return records_output
        record = self.db.session.execute(
            self.db.select(ProjectCharge).where(ProjectCharge.name == name)
        ).scalar()
        if record is not None:
            record_output = {
                "id": record.id,
                "name": record.name,
                "level": record.level_name.name,
                "salary": record.salary,
            }
            return record_output

    def modify_charge(self, name, level, salary):
        record = self.db.session.execute(
            self.db.select(ProjectCharge).where(ProjectCharge.name == name)
        ).scalar()
        if record is not None:
            record.name = name
            record.level = level
            record.salary = salary
            self.db.session.commit()
            return True
        return False

    def delete_charge(self, name):
        record = self.db.session.execute(
            self.db.select(ProjectCharge).where(ProjectCharge.name == name)
        ).scalar()
        if record is not None:
            self.db.session.delete(record)
            self.db.session.commit()
            return True
        return False

    def add_type(self, name):
        record = ProjectType(name=name)
        self.db.session.add(record)
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            return True

    def get_type(self, name=""):
        if name == "":
            print("name", name)
            records = (
                self.db.session.execute(
                    self.db.select(ProjectType).order_by(ProjectType.id)
                )
                .scalars()
                .all()
            )
            print("records", records)
            if len(records) > 0:
                records_output = [{"id": i.id, "name": i.name} for i in records]
                print(records_output)
                return records_output
        else:
            record = self.db.session.execute(
                self.db.select(ProjectType).where(ProjectType.name == name)
            ).scalar()
            if record is not None:
                record_output = {"id": record.id, "name": record.name}
                return record_output

    def delete_type(self, name):
        record = self.db.session.execute(
            self.db.select(ProjectType).where(ProjectType.name == name)
        ).scalar()
        if record is not None:
            self.db.session.delete(record)
            self.db.session.commit()
            return True
        return False

    def add_status(self, name):
        record = ProjectStatus(name=name)
        self.db.session.add(record)
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            return True

    def get_status(self, name=""):
        if name == "":
            records = (
                self.db.session.execute(
                    self.db.select(ProjectStatus).order_by(ProjectStatus.id)
                )
                .scalars()
                .all()
            )
            if records:
                records_output = [{"id": i.id, "name": i.name} for i in records]
                return records_output
        record = self.db.session.execute(
            self.db.select(ProjectStatus).where(ProjectStatus.name == name)
        ).scalar()
        if record is not None:
            record_output = {"id": record.id, "name": record.name}
            return record_output

    def delete_status(self, name):
        record = self.db.session.execute(
            self.db.select(ProjectStatus).where(ProjectStatus.name == name)
        ).scalar()
        if record is not None:
            self.db.session.delete(record)
            self.db.session.commit()
            return True
        return False

    def add_project(
        self,
        name,
        start_time,
        end_time,
        type_id,
        m_id_list,
        p_id_list,
        status_id,
        payment,
        balance_payment,
    ):

        tax = payment * 0.06
        profit = payment - tax
        profit_rate = round(profit / payment, 2)
        record = Project(
            name=name,
            start_time=start_time,
            end_time=end_time,
            type_id=type_id,
            status_id=status_id,
            profit=profit,
            profit_rate=profit_rate,
            tax=tax,
            balance_payment=balance_payment,
            payment=payment,
            cost=0,
        )
        self.db.session.add(record)
        try:
            self.db.session.flush()
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            self.collect_charger_data(m_id_list, p_id_list, record)
            return True

    def get_project_list(self):
        records = (
            self.db.session.execute(
                self.db.select(Project).order_by(Project.start_time)
            )
            .scalars()
            .all()
        )

        records_output = [
            {
                "id": i.id,
                "name": i.name,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "type_id": i.type_name.name,
                "status_id": i.status_name.name,
                "m_charges": [
                    {"charge": c.name, "level": c.level_name.name, "salary": c.salary}
                    for c in i.m_charges
                ],
                "p_charges": [
                    {"charge": c.name, "level": c.level_name.name, "salary": c.salary}
                    for c in i.p_charges
                ],
                "profit": f"{i.profit:,.2f}",
                "profit_rate": f"{i.profit_rate:.2%}",
                "tax": f"{i.tax:,.2f}",
                "balance_payment": f"{i.balance_payment:,.2f}",
                "payment": f"{i.payment:,.2f}",
                "cost": f"{i.cost:,.2f}",
            }
            for i in records
        ]
        if records_output:
            return records_output

    # TODO
    def get_project(
        self, name=None, _id=None, charge_m_id=None, charge_p_id=None, type_id=None
    ):
        conditions = []
        if _id is not None:
            conditions.append(Project.id == _id)
            i = self.db.session.execute(
                self.db.select(Project).where(and_(*conditions))
            ).scalar()
            record_output = {
                "id": i.id,
                "name": i.name,
                "start_time": i.start_time[:10],
                "end_time": i.end_time[:10],
                "type_id": i.type_id,
                "status_id": i.status_id,
                "m_charges": [
                    {
                        "id": c.id,
                        "charge": c.name,
                        "level": c.level_name.name,
                        "salary": c.salary,
                    }
                    for c in i.m_charges
                ],
                "p_charges": [
                    {
                        "id": c.id,
                        "charge": c.name,
                        "level": c.level_name.name,
                        "salary": c.salary,
                    }
                    for c in i.p_charges
                ],
                "profit": i.profit,
                "profit_rate": i.profit_rate,
                "tax": i.tax,
                "balance_payment": i.balance_payment,
                "payment": i.payment,
                "cost": i.cost,
            }
            if record_output:
                return record_output
        if name is not None:
            conditions.append(Project.name.like(f"%{name}%"))
        #     TODO
        if charge_m_id is not None:
            conditions.append(Project.m_charges.any(ProjectCharge.id == charge_m_id))
        #     TODO
        if charge_p_id is not None:
            conditions.append(Project.p_charges.any(ProjectCharge.id == charge_p_id))
        if type_id is not None:
            conditions.append(Project.type_id == type_id)
        # print(conditions)
        records = (
            self.db.session.execute(
                self.db.select(Project).where(and_(*conditions)).order_by(Project.id)
            )
            .scalars()
            .all()
        )
        records_output = [
            {
                "id": i.id,
                "name": i.name,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "type_id": i.type_name.name,
                "status_id": i.status_name.name,
                "m_charges": [
                    {
                        "id": c.id,
                        "charge": c.name,
                        "level": c.level_name.name,
                        "salary": c.salary,
                    }
                    for c in i.m_charges
                ],
                "p_charges": [
                    {
                        "id": c.id,
                        "charge": c.name,
                        "level": c.level_name.name,
                        "salary": c.salary,
                    }
                    for c in i.p_charges
                ],
                "profit": f"{i.profit:,.2f}",
                "profit_rate": f"{i.profit_rate:.2%}",
                "tax": f"{i.tax:,.2f}",
                "balance_payment": f"{i.balance_payment:,.2f}",
                "payment": f"{i.payment:,.2f}",
                "cost": f"{i.cost:,.2f}",
            }
            for i in records
        ]
        if records_output:
            return records_output

    def update_project(
        self,
        _id,
        name,
        start_time,
        end_time,
        type_id,
        m_id_list,
        p_id_list,
        status_id,
        payment,
        balance_payment,
    ):
        i = self.db.session.execute(
            self.db.select(Project).where(Project.id == _id)
        ).scalar()
        tax = payment * 0.06
        profit = payment - i.cost - tax
        profit_rate = round(profit / payment, 2)

        i.name = name
        i.start_time = start_time
        i.end_time = end_time
        i.type_id = type_id
        i.status_id = status_id
        i.balance_payment = balance_payment
        i.payment = payment
        i.profit = profit
        i.profit_rate = profit_rate
        i.tax = tax
        try:
            self.db.session.flush()
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            self.collect_charger_data(m_id_list, p_id_list, i)
            return True

    def delete_project(self, _id):
        record = self.db.session.execute(
            self.db.select(Project).where(Project.id == _id)
        ).scalar()
        if record is not None:
            self.db.session.delete(record)
            self.db.session.commit()
            return True
        return False

    def count_sum(self):
        sum_of_payment = self.db.session.query(func.sum(Project.payment)).scalar()
        sum_of_salary = (
            self.db.session.query(func.sum(ProjectCharge.salary)).scalar() * 12
        )
        sum_of_profit = (
            self.db.session.query(func.sum(Project.profit)).scalar() - sum_of_salary
        )
        sum_of_balance_payment = self.db.session.query(
            func.sum(Project.balance_payment)
        ).scalar()

        return {
            "sum_of_payment": f"{sum_of_payment:,.2f}",
            "sum_of_profit": f"{sum_of_profit:,.2f}",
            "sum_of_balance_payment": f"{sum_of_balance_payment:,.2f}",
            "sum_of_salary": f"{sum_of_salary:,.2f}",
        }

    def add_administrator(self, user_name, password):
        record = Admin(user_name=user_name, password=password)
        self.db.session.add(record)
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            return True

    def get_administrator(self):
        records = (
            self.db.session.execute(self.db.select(Admin).order_by(Admin.id))
            .scalars()
            .all()
        )
        if records:
            records_output = [
                {"id": i.id, "admin": i.user_name, "password": i.password}
                for i in records
            ]
            return records_output

    def administrator_mapping(self):
        admin_list = self.get_administrator()
        print("admin_list")
        admin_mapping = {i["admin"]: i for i in admin_list}
        return admin_mapping

    def add_cost(self, _id, project_id, name, cost, remark=None):
        record = ProjectCost(name=name, project_id=project_id, cost=cost, remark=remark)
        self.db.session.add(record)
        try:
            self.db.session.flush()
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            # 更新项目成本，利润和利润率
            self.update_project_cost(project_id, cost)
            return {
                "id": record.id,
                "project_id": record.project_id,
                "name": record.name,
                "cost": record.cost,
                "remark": record.remark,
            }

    def update_project_cost(self, _id, cost):
        record = self.db.session.execute(
            self.db.select(Project).where(Project.id == _id)
        ).scalar()
        record.cost = record.cost + cost
        record.profit = record.profit - cost
        record.profit_rate = round(record.profit / record.payment, 2)
        self.db.session.commit()

    def get_cost(self, id):
        records = (
            self.db.session.execute(
                self.db.select(ProjectCost)
                .where(ProjectCost.project_id == id)
                .order_by(ProjectCost.id)
            )
            .scalars()
            .all()
        )

        if len(records) > 0:
            return [
                {
                    "id": record.id,
                    "project_id": record.project_id,
                    "name": record.name,
                    "cost": record.cost,
                    "remark": record.remark,
                }
                for record in records
            ]

    def delete_cost(self, id):
        record = self.db.session.execute(
            self.db.select(ProjectCost).where(ProjectCost.id == id)
        ).scalar()
        if record is not None:
            record.total_cost.cost -= record.cost
            self.db.session.delete(record)
            self.db.session.commit()
            return True
        return False

    def out_data(self):
        records = (
            self.db.session.execute(self.db.select(Project).order_by(Project.id))
            .scalars()
            .all()
        )
        print(records)
        dataframe = pandas.DataFrame(
            [
                (
                    i.id,
                    i.name,
                    f"{i.payment:,.2f}",
                    f"{i.cost:,.2f}",
                    f"{i.balance_payment:,.2f}",
                    f"{i.tax:,.2f}",
                    f"{i.profit:,.2f}",
                    f"{i.profit_rate:.2%}",
                    i.start_time,
                    i.end_time,
                    (
                        [f"{c.name}|{c.level_name.name}" for c in i.m_charges]
                        if len([f"{c.name}|{c.level_name.name}" for c in i.m_charges])
                        > 0
                        else ""
                    ),
                    (
                        [f"{c.name}|{c.level_name.name}" for c in i.p_charges]
                        if len([f"{c.name}|{c.level_name.name}" for c in i.p_charges])
                        > 0
                        else ""
                    ),
                )
                for i in records
            ],
            columns=[
                "项目编号",
                "项目名称",
                "项目金额",
                "项目成本",
                "项目尾款",
                "项目税款",
                "项目利润",
                "项目利润率",
                "项目开始时间",
                "项目结束时间",
                "项目管理",
                "项目专家",
            ],
        )
        excel_name = "output.xlsx"
        dataframe.to_excel(excel_name, index=False)
        return send_file(excel_name, as_attachment=True)

    def add_level(self, name):
        record = Level(name=name)
        self.db.session.add(record)
        try:
            self.db.session.flush()
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            return {"id": record.id, "name": record.name}

    def get_level(self):
        records = (
            self.db.session.execute(self.db.select(Level).order_by(Level.id))
            .scalars()
            .all()
        )
        if len(records) > 0:
            return [{"id": record.id, "name": record.name} for record in records]

    def collect_charger_data(self, m_id_list, p_id_list, project):
        project.m_charges = []
        project.p_charges = []
        self.db.session.commit()
        if m_id_list:
            for i in m_id_list:
                record = self.db.session.execute(
                    self.db.select(ProjectCharge).where(ProjectCharge.id == i)
                ).scalar()
                project.m_charges.append(record)
        if p_id_list:
            for i in p_id_list:
                record = self.db.session.execute(
                    self.db.select(ProjectCharge).where(ProjectCharge.id == i)
                ).scalar()
                project.p_charges.append(record)
        self.db.session.commit()
