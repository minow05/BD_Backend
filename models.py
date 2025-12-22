from flask_sqlalchemy import SQLAlchemy
import enum;

db = SQLAlchemy()

class TaskStatus(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    DONE = "DONE"
    BLOCKED = "BLOCKED"

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    street = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))


class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    login = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))

    supervisor_id = db.Column(db.Integer, db.ForeignKey("employee.id"))

    role = db.relationship("Role")
    address = db.relationship("Address")
    supervisor = db.relationship("Employee", remote_side=[id])


class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    manager_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    manager = db.relationship("Employee")


class Team(db.Model):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    section_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    manager_id = db.Column(db.Integer, db.ForeignKey("employee.id"))

    section = db.relationship("Section")
    manager = db.relationship("Employee")


# association table
class EmployeeTeam(db.Model):
    __tablename__ = "employee_team"
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), primary_key=True)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    deadline = db.Column(db.String(20))
    status = db.Column(
        db.Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.TODO
    )

    created_at = db.Column(db.String(30))


class TaskAssignment(db.Model):
    __tablename__ = "task_assignment"
    id = db.Column(db.Integer, primary_key=True)

    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))

    section_id = db.Column(db.Integer, db.ForeignKey("section.id"), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=True)

    task = db.relationship("Task")
    section = db.relationship("Section")
    team = db.relationship("Team")
    employee = db.relationship("Employee")
