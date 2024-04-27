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
SUPER_ADMIN = [1, 2]

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

project_admin_association = db.Table(
    "project_admin_link",
    db.Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    db.Column("admin_id", Integer, ForeignKey("admin.id"), primary_key=True),
)


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
    month: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
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


class Admin(db.Model):
    __tablename__ = "admin"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    user_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    admin_projects = relationship(
        "Project", secondary=project_admin_association, back_populates="project_admin"
    )


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
    not_paid: Mapped[float] = mapped_column(Float, default=0)
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
    project_admin = relationship(
        "Admin",
        secondary=project_admin_association,
        back_populates="admin_projects",
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
    month: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    remark: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class Database:
    def __init__(self):
        self.db = db

    def create_table(self):
        self.db.create_all()

    def add_charge(self, name, level, salary, month):
        record = ProjectCharge(name=name, level=level, salary=salary, month=month)
        self.db.session.add(record)
        try:
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            return True

    def get_charge(self, _id=None):
        if not _id:
            records = (
                self.db.session.execute(
                    self.db.select(ProjectCharge).order_by(ProjectCharge.id)
                )
                .scalars()
                .all()
            )
            # print(records)
            if records:
                records_output = [
                    {
                        "id": i.id,
                        "name": i.name,
                        "level": i.level_name.name,
                        "salary": i.salary,
                        "month": i.month,
                        "m_projects": [c.name for c in i.m_projects],
                        "p_projects": [c.name for c in i.p_projects],
                    }
                    for i in records
                ]
                return records_output
        record = self.db.session.execute(
            self.db.select(ProjectCharge).where(ProjectCharge.id == _id)
        ).scalar()
        if record is not None:
            record_output = {
                "id": record.id,
                "name": record.name,
                "level": record.level_name.name,
                "month": record.month,
                "salary": record.salary,
            }
            return record_output

    def modify_charge(self, _id, name, level, salary, month):
        record = self.db.session.execute(
            self.db.select(ProjectCharge).where(ProjectCharge.id == _id)
        ).scalar()
        # print(record)
        if record is not None:
            record.name = name
            record.level = level
            record.salary = salary
            record.month = month
            self.db.session.commit()
            return True
        return False

    def delete_charge(self, _id):
        record = self.db.session.execute(
            self.db.select(ProjectCharge).where(ProjectCharge.id == _id)
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
            # print("name", name)
            records = (
                self.db.session.execute(
                    self.db.select(ProjectType).order_by(ProjectType.id)
                )
                .scalars()
                .all()
            )
            # print("records", records)
            if len(records) > 0:
                records_output = [{"id": i.id, "name": i.name} for i in records]
                # print(records_output)
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
        payment = round(payment, 2)
        tax = round(payment * 0.06, 2)
        profit = round(payment - tax, 2)
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
            # self.update_super_admin_projects(record)
            self.collect_charger_data(m_id_list, p_id_list, record)
            return True

    def get_project_list(self, admin_id):
        records = (
            self.db.session.execute(
                self.db.select(Project).order_by(Project.start_time)
            )
            .scalars()
            .all()
        )
        if admin_id == "0":
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
                            "charge": c.name,
                            "level": c.level_name.name,
                            "salary": c.salary,
                        }
                        for c in i.m_charges
                    ],
                    "p_charges": [
                        {
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
                    "not_paid": f"{i.not_paid:,.2f}",
                }
                for i in records
            ]
        else:
            admin_projects = self.get_admin_projects(admin_id)
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
                            "charge": c.name,
                            "level": c.level_name.name,
                            "salary": c.salary,
                        }
                        for c in i.m_charges
                    ],
                    "p_charges": [
                        {
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
                    "not_paid": f"{i.not_paid:,.2f}",
                }
                for i in records
                if i in admin_projects
            ]
        if records_output:
            return records_output

    # TODO
    def get_project(
        self,
        admin_id,
        name=None,
        _id=None,
        charge_m_id=None,
        charge_p_id=None,
        type_id=None,
    ):
        # print(admin_id, name, _id, charge_p_id, charge_m_id, type_id)
        admin_projects = self.get_admin_projects(admin_id)
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
                "not_paid": i.not_paid,
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
        dashboard = self.count_sum(conditions)
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
                "not_paid": f"{i.not_paid:,.2f}",
                "dashboard": dashboard,
            }
            for i in records
            if i in admin_projects
        ]
        # print(records_output)
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
        payment = round(payment, 2)
        tax = round(payment * 0.06, 2)
        profit = round(payment - i.cost - tax, 2)
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

    def count_sum(self, conditions=None):
        sum_of_salary = self.db.session.query(
            func.sum(ProjectCharge.salary * func.coalesce(ProjectCharge.month, 12))
        ).scalar()
        if conditions is None:
            sum_of_payment = self.db.session.query(func.sum(Project.payment)).scalar()

            sum_of_profit = (
                self.db.session.query(func.sum(Project.profit)).scalar() - sum_of_salary
            )
            sum_of_balance_payment = self.db.session.query(
                func.sum(Project.balance_payment)
            ).scalar()
            sum_of_cost = self.db.session.query(func.sum(ProjectCost.cost)).scalar()
        else:
            sum_of_payment = (
                self.db.session.query(func.sum(Project.payment))
                .where(and_(*conditions))
                .scalar()
            )

            sum_of_profit = (
                self.db.session.query(func.sum(Project.profit))
                .where(and_(*conditions))
                .scalar()
            )

            sum_of_balance_payment = (
                self.db.session.query(func.sum(Project.balance_payment))
                .where(and_(*conditions))
                .scalar()
            )

            sum_of_cost = (
                self.db.session.query(func.sum(ProjectCost.cost))
                .where(and_(*conditions))
                .scalar()
            )
            print(sum_of_cost)

            if sum_of_payment is None:
                sum_of_payment = 0
                sum_of_profit = 0
                sum_of_balance_payment = 0
                sum_of_cost = 0
        return {
            "sum_of_payment": f"{sum_of_payment:,.2f}",
            "sum_of_profit": f"{sum_of_profit:,.2f}",
            "sum_of_balance_payment": f"{sum_of_balance_payment:,.2f}",
            "sum_of_salary": f"{sum_of_salary:,.2f}",
            "sum_of_cost": f"{sum_of_cost:,.2f}",
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
                {
                    "id": i.id,
                    "admin": i.user_name,
                    "password": i.password,
                    "projects": [
                        {
                            "id": i.id,
                            "name": i.name,
                        }
                        for i in i.admin_projects
                    ],
                }
                for i in records
            ]
            return records_output

    def administrator_mapping(self):
        admin_list = self.get_administrator()
        # print("admin_list")
        admin_mapping = {i["admin"]: i for i in admin_list}
        return admin_mapping

    def update_not_paid(self, project_id):
        conditions = [ProjectCost.project_id == project_id, ProjectCost.status == 0]
        sum_of_not_paid = (
            self.db.session.query(func.sum(ProjectCost.cost))
            .where(and_(*conditions))
            .scalar()
        )
        # print(sum_of_not_paid)
        record = self.db.session.execute(
            self.db.select(Project).where(Project.id == project_id)
        ).scalar()
        # print(record.not_paid)
        if sum_of_not_paid is None:
            record.not_paid = 0.0
        else:
            record.not_paid = sum_of_not_paid
        self.db.session.commit()

    def add_cost(self, project_id, name, cost, month=1, remark=None, status=0):
        record = ProjectCost(
            name=name,
            project_id=project_id,
            cost=round(cost, 2),
            remark=remark,
            status=status,
            month=month,
        )
        self.db.session.add(record)
        try:
            self.db.session.flush()
            self.db.session.commit()
        except exc.IntegrityError:
            return False
        else:
            self.update_not_paid(project_id)
            # 更新项目成本，利润和利润率
            self.update_project_cost(project_id, round(cost, 2))
            return {
                "id": record.id,
                "project_id": record.project_id,
                "name": record.name,
                "cost": record.cost,
                "remark": record.remark,
                "status": record.status,
                "month": record.month,
            }

    def modify_cost(
        self,
        id,
        name,
        cost,
        month,
        remark,
        status,
    ):
        record = self.db.session.execute(
            self.db.select(ProjectCost).where(ProjectCost.id == id)
        ).scalar()
        if record:
            origin_cost = record.cost
            record.name = name
            record.cost = round(cost, 2)
            record.remark = remark
            record.status = status
            record.month = month

            try:
                self.db.session.commit()
            except exc.IntegrityError:
                return False
            else:
                self.update_project_cost(record.project_id, round(cost, 2), origin_cost)
                self.update_not_paid(record.project_id)
                return {
                    "id": record.id,
                    "project_id": record.project_id,
                    "name": record.name,
                    "cost": record.cost,
                    "remark": record.remark,
                    "status": record.status,
                    "month": record.month,
                }

    def update_project_cost(self, _id, cost, origin_cost=None):
        record = self.db.session.execute(
            self.db.select(Project).where(Project.id == _id)
        ).scalar()
        if origin_cost:
            record.cost = round(record.cost - origin_cost + cost, 2)
            record.profit = round(record.profit + origin_cost - cost, 2)
        else:
            record.cost = round(record.cost + cost, 2)
            record.profit = round(record.profit - cost, 2)
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
                    "status": record.status,
                    "month": record.month,
                }
                for record in records
            ]

    def get_cost_overall(self, month):
        conditions = []
        if month == 13:
            records = (
                self.db.session.execute(
                    self.db.select(ProjectCost).order_by(ProjectCost.id)
                )
                .scalars()
                .all()
            )
        else:
            records = (
                self.db.session.execute(
                    self.db.select(ProjectCost)
                    .where(ProjectCost.month == month)
                    .order_by(ProjectCost.id)
                )
                .scalars()
                .all()
            )
            conditions.append(ProjectCost.month == month)
        dashboard = self.count_sum(conditions)
        if len(records) > 0:
            return [
                {
                    "id": record.id,
                    "project_id": record.project_id,
                    "project": record.total_cost.name,
                    "name": record.name,
                    "cost": record.cost,
                    "remark": record.remark,
                    "status": record.status,
                    "month": record.month,
                    "dashboard": dashboard,
                }
                for record in records
            ]

    def get_single_cost(self, c_id):
        record = self.db.session.execute(
            self.db.select(ProjectCost).where(ProjectCost.id == c_id)
        ).scalar()
        if record:
            return {
                "id": record.id,
                "project_id": record.project_id,
                "name": record.name,
                "cost": record.cost,
                "remark": record.remark,
                "status": record.status,
                "month": record.month,
            }

    def delete_cost(self, id, _id):
        record = self.db.session.execute(
            self.db.select(ProjectCost).where(ProjectCost.id == id)
        ).scalar()
        if record is not None:
            self.update_project_cost(_id, -record.cost)
            self.db.session.delete(record)
            self.db.session.commit()
            self.update_not_paid(_id)
            return True
        return False

    def out_data(self):
        try:
            records = (
                self.db.session.execute(self.db.select(Project).order_by(Project.id))
                .scalars()
                .all()
            )
            # print(records)
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
                            if len(
                                [f"{c.name}|{c.level_name.name}" for c in i.m_charges]
                            )
                            > 0
                            else ""
                        ),
                        (
                            [f"{c.name}|{c.level_name.name}" for c in i.p_charges]
                            if len(
                                [f"{c.name}|{c.level_name.name}" for c in i.p_charges]
                            )
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
        except Exception as e:
            # 显示错误信息
            return {"error": str(e)}

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

    def add_admin_projects(self, project_list, admin_id):
        admin_record = self.db.session.execute(
            self.db.select(Admin).where(Admin.id == admin_id)
        ).scalar()
        # print(admin_record)
        if admin_record:
            admin_record.admin_projects = []
            self.db.session.commit()
            if project_list:
                for i in project_list:
                    record = self.db.session.execute(
                        self.db.select(Project).where(Project.id == i)
                    ).scalar()
                    admin_record.admin_projects.append(record)
                    # print(admin_record.admin_projects)
        self.db.session.commit()
        return {
            "id": admin_record.id,
            "admin": admin_record.user_name,
            "password": admin_record.password,
            "projects": [i for i in admin_record.admin_projects],
        }

    def get_admin_projects(self, admin_id, checked=None):
        admin_record = self.db.session.execute(
            self.db.select(Admin).where(Admin.id == admin_id)
        ).scalar()
        if admin_record is not None:
            if checked is None:
                return [i for i in admin_record.admin_projects]
            else:
                return [
                    {"id": i.id, "name": i.name} for i in admin_record.admin_projects
                ]
        else:
            return []

    # def update_super_admin_projects(self, project):
    #     id = project.id
    #     print(id)
    #     record = self.db.session.execute(
    #         self.db.select(Project).where(Project.id == id)
    #     )
    #     print("new_project", record)
    #     for i in SUPER_ADMIN:
    #         exist_project_list = self.get_admin_projects(i)
    #         exist_project_list.append(record)
    #         print("the list", exist_project_list, i)
    #         self.add_admin_projects(exist_project_list, i)

    def read_file(self, file, _id):
        df = pandas.read_excel(file, skiprows=2)
        df.rename(
            columns={
                "费用类型": "category",
                "内容": "name",
                "成本": "cost",
                "付款备注（填写公司或者劳务费姓名）": "remark",
            },
            inplace=True,
        )
        # print(df)
        df.dropna(how="all", axis="index", inplace=True)
        df.ffill(inplace=True)
        df["cost"] = df["cost"].round(2)
        for idx, row in df.iterrows():
            if isinstance(row["remark"], float) or isinstance(row["remark"], int):
                continue
            # print(idx, row["name"], row["cost"], row["remark"], type(row["remark"]))
            self.add_cost(_id, str(row["name"]), row["cost"], str(row["remark"]))
