from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Float, String, ForeignKey, exc, and_, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
import pandas
from flask import send_file


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


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


class ProjectCharge(db.Model):
    __tablename__ = "project_charge"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    related_project = relationship("Project", backref="charge_name")


class ProjectStatus(db.Model):
    __tablename__ = "project_status"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    related_project = relationship("Project", backref="status_name")


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
    charge_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project_charge.id"), nullable=False
    )
    start_time: Mapped[str] = mapped_column(String, nullable=False)
    end_time: Mapped[str] = mapped_column(String, nullable=False)
    status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project_status.id"), nullable=False
    )
    relationship("ProjectCost", backref="total_cost")


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

    def add_charge(self, name):
        record = ProjectCharge(name=name)
        self.db.session.add(record)
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            return True

    def get_charge(self, name=None):
        if name is None:
            records = (
                self.db.session.execute(
                    self.db.select(ProjectCharge).order_by(ProjectCharge.id)
                )
                .scalars()
                .all()
            )
            if records:
                records_output = [{"id": i.id, "name": i.name} for i in records]
                return records_output
        record = self.db.session.execute(
            self.db.select(ProjectCharge).where(ProjectCharge.name == name)
        ).scalar()
        if record is not None:
            record_output = {"id": record.id, "name": record.name}
            return record_output

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

    def get_type(self, name=None):
        if name is None:
            records = (
                self.db.session.execute(
                    self.db.select(ProjectType).order_by(ProjectType.id)
                )
                .scalars()
                .all()
            )
            if records:
                records_output = [{"id": i.id, "name": i.name} for i in records]
                return records_output
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

    def get_status(self, name=None):
        if name is None:
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
        charge_id,
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
            charge_id=charge_id,
            profit=profit,
            profit_rate=profit_rate,
            tax=tax,
            balance_payment=balance_payment,
            payment=payment,
            cost=0,
        )
        self.db.session.add(record)
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
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
                "charge_id": i.charge_name.name,
                "profit": f"{i.profit:,.2f}",
                "profit_rate": f"{i.profit_rate:.2%}",
                "tax": f"{i.tax:,.2f}",
                "balance_payment": f"{i.balance_payment:,.2f}",
                "payment": f"{i.payment:,.2f}",
                "cost": f"{0 if self.db.session.query(func.sum(ProjectCost.cost)).filter(ProjectCost.id == i.id).scalar() is None else self.db.session.query(func.sum(ProjectCost.cost)).filter(ProjectCost.id == i.id).scalar():,.2f}",
            }
            for i in records
        ]
        if records_output:
            return records_output

    def get_project(self, name=None, _id=None, charge_id=None, type_id=None):
        conditions = []
        if _id is not None:
            conditions.append(Project.id == _id)
            i = self.db.session.execute(
                self.db.select(Project).where(and_(*conditions))
            ).scalar()
            record_output = {
                "id": i.id,
                "name": i.name,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "type_id": i.type_id,
                "status_id": i.status_id,
                "charge_id": i.charge_id,
                "profit": i.profit,
                "profit_rate": i.profit_rate,
                "tax": i.tax,
                "balance_payment": i.balance_payment,
                "payment": i.payment,
                "cost": (
                    0
                    if self.db.session.query(func.sum(ProjectCost.cost))
                    .filter(ProjectCost.id == i.id)
                    .scalar()
                    is None
                    else self.db.session.query(func.sum(ProjectCost.cost))
                    .filter(ProjectCost.id == i.id)
                    .scalar()
                ),
            }
            if record_output:
                return record_output
        if name is not None:
            conditions.append(Project.name.like(f"%{name}%"))
        if charge_id is not None:
            conditions.append(Project.charge_id == charge_id)
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
                "charge_id": i.charge_name.name,
                "profit": f"{i.profit:,.2f}",
                "profit_rate": f"{i.profit_rate:.2%}",
                "tax": f"{i.tax:,.2f}",
                "balance_payment": f"{i.balance_payment:,.2f}",
                "payment": f"{i.payment:,.2f}",
                "cost": f"{0 if self.db.session.query(func.sum(ProjectCost.cost)).filter(ProjectCost.id == i.id).scalar() is None else self.db.session.query(func.sum(ProjectCost.cost)).filter(ProjectCost.id == i.id).scalar():,.2f}",
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
        charge_id,
        status_id,
        payment,
        balance_payment,
    ):
        i = self.db.session.execute(
            self.db.select(Project).where(Project.id == _id)
        ).scalar()
        tax = payment * 0.06
        profit = (
            payment
            - (
                0
                if self.db.session.query(func.sum(ProjectCost.cost))
                .filter(ProjectCost.id == i.id)
                .scalar()
                is None
                else self.db.session.query(func.sum(ProjectCost.cost))
                .filter(ProjectCost.id == i.id)
                .scalar()
            )
            - tax
        )
        profit_rate = round(profit / payment, 2)

        i.name = name
        i.start_time = start_time
        i.end_time = end_time
        i.type_id = type_id
        i.status_id = status_id
        i.charge_id = charge_id
        i.balance_payment = balance_payment
        i.payment = payment
        i.profit = profit
        i.profit_rate = profit_rate
        i.tax = tax
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
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
        sum_of_profit = self.db.session.query(func.sum(Project.profit)).scalar()
        sum_of_balance_payment = self.db.session.query(
            func.sum(Project.balance_payment)
        ).scalar()
        return {
            "sum_of_payment": f"{sum_of_payment:,.2f}",
            "sum_of_profit": f"{sum_of_profit:,.2f}",
            "sum_of_balance_payment": f"{sum_of_balance_payment:,.2f}",
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
        admin_mapping = {i["admin"]: i for i in admin_list}
        return admin_mapping

    def add_cost(self, _id, name, cost, remark=None):
        pass
        # TODO

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
                    i.payment,
                    i.cost,
                    i.balance_payment,
                    i.tax,
                    i.profit,
                    i.profit_rate,
                    i.start_time,
                    i.end_time,
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
            ],
        )
        excel_name = "output.xlsx"
        dataframe.to_excel(excel_name, index=False)
        return send_file(excel_name, as_attachment=True)
