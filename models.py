from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

# ======================
# ENUM
# ======================
class TaskStatus(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    BLOCKED = "BLOCKED"


# ======================
# ADDRESS
# ======================
class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    street = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    house_number = db.Column(db.String(10))
    apartment_number = db.Column(db.String(10), nullable=True)


# ======================
# EMPLOYEE (BASE)
# ======================
class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    pesel = db.Column(db.String(20))

    phone = db.Column(db.String(30))
    email = db.Column(db.String(50))

    login = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))

    hire_date = db.Column(db.String(20))
    fire_date = db.Column(db.String(20), nullable=True)

    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    address = db.relationship("Address")

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "employee"
    }


# ======================
# ROLE ENTITIES
# ======================
class StudioHead(Employee):
    __tablename__ = "studio_head"
    id = db.Column(db.Integer, db.ForeignKey("employee.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "studio_head"}


class SectionManager(Employee):
    __tablename__ = "section_manager"
    id = db.Column(db.Integer, db.ForeignKey("employee.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "section_manager"}


class TeamManager(Employee):
    __tablename__ = "team_manager"
    id = db.Column(db.Integer, db.ForeignKey("employee.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "team_manager"}


class TeamMember(Employee):
    __tablename__ = "team_member"
    id = db.Column(db.Integer, db.ForeignKey("employee.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "team_member"}


# ======================
# SECTION
# ======================
class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    manager_id = db.Column(db.Integer, db.ForeignKey("section_manager.id"))
    manager = db.relationship("SectionManager")


# ======================
# TEAM
# ======================
class Team(db.Model):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    section_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    manager_id = db.Column(db.Integer, db.ForeignKey("team_manager.id"))

    section = db.relationship("Section")
    manager = db.relationship("TeamManager")


# ======================
# TEAM MEMBER <-> TEAM (M:N)
# ======================
class TeamMembership(db.Model):
    __tablename__ = "team_membership"
    team_member_id = db.Column(
        db.Integer,
        db.ForeignKey("team_member.id"),
        primary_key=True
    )
    team_id = db.Column(
        db.Integer,
        db.ForeignKey("team.id"),
        primary_key=True
    )


# ======================
# GAME
# ======================
class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    studio_head_id = db.Column(db.Integer, db.ForeignKey("studio_head.id"))

    studio_head = db.relationship("StudioHead")


# ======================
# TASK (BASE)
# ======================
class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.Text)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))

    status = db.Column(db.Enum(TaskStatus))


# ======================
# TASK – SECTION
# ======================
class SectionTask(db.Model):
    __tablename__ = "section_task"
    id = db.Column(db.Integer, primary_key=True)

    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))

    task = db.relationship("Task")
    section = db.relationship("Section")
    game = db.relationship("Game")


# ======================
# TASK – TEAM
# ======================
class TeamTask(db.Model):
    __tablename__ = "team_task"
    id = db.Column(db.Integer, primary_key=True)

    section_task_id = db.Column(db.Integer, db.ForeignKey("section_task.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))

    section_task = db.relationship("SectionTask")
    team = db.relationship("Team")


# ======================
# TASK – EMPLOYEE
# ======================
class EmployeeTask(db.Model):
    __tablename__ = "employee_task"
    id = db.Column(db.Integer, primary_key=True)

    team_task_id = db.Column(db.Integer, db.ForeignKey("team_task.id"))
    team_member_id = db.Column(db.Integer, db.ForeignKey("team_member.id"))

    team_task = db.relationship("TeamTask")
    team_member = db.relationship("TeamMember")
