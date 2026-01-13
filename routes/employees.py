from flask import Blueprint, request, jsonify
from models import db, Employee, TeamMember, TeamMembership, Team, StudioHead, SectionManager, TeamManager
from werkzeug.security import check_password_hash
employees_bp = Blueprint("employees", __name__)


@employees_bp.post("/")
def create_employee():
    data = request.json

    employee = TeamMember(
        first_name=data["first_name"],
        last_name=data["last_name"],
        login=data["login"],
        password_hash=data["password"]
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({"id": employee.id}), 201


@employees_bp.get("/")
def get_employees():
    employees = TeamMember.query.all()

    return jsonify([
        {
            "id": e.id,
            "first_name": e.first_name,
            "last_name": e.last_name
        }
        for e in employees
    ])
@employees_bp.get("/employee/id/<int:id>")
def get_employee_id(id):

    employeee = (
        db.session.query(Employee)
        .filter(Employee.id == id)
    )
    return jsonify([
        {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "pesel": employee.pesel,
            "phone": employee.phone,
            "email": employee.email,
            "hire_date": employee.hire_date,
        }
        for employee in employeee   
    ])
    
@employees_bp.get("/employee/<string:employee_login>/<string:employee_password>")
def get_employee(employee_login, employee_password):
    position = ""
    employeee = (
        db.session.query(Employee)
        .filter(Employee.login == employee_login)
    )
    for employee in employeee:
        right_password = employee.password_hash
    passw = check_password_hash(right_password,employee_password)
    if passw == True:
        position = "employee"
        studioHead = StudioHead.query.all()
        sectionManager = SectionManager.query.all()
        teamManager = TeamManager.query.all()
        id = employee.id
        for e in studioHead:
            if id == e.id:
                position = "studioHead"
        for e in sectionManager:
            if id == e.id:
                position = "sectionManager"
        for e in teamManager:
            if id == e.id:
                position = "teamManager"
        return jsonify([
            {
                "status": "good",
                "id": employee.id,
                "position": position,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "pesel": employee.pesel,
                "phone": employee.phone,
                "email": employee.email,
                "hire_date": employee.hire_date,
            }
            for employee in employeee   
        ])
    else:
        return jsonify([
            {
            "status": "bad",
            }
        ])

@employees_bp.get("/team/<int:team_id>")
def get_employees_of_team(team_id):
    employees = (
        db.session.query(TeamMember)
        .join(TeamMembership)
        .filter(TeamMembership.team_id == team_id)
        .all()
    )

    return jsonify([
        {
            "id": e.id,
            "first_name": e.first_name,
            "last_name": e.last_name
        }
        for e in employees
    ])

@employees_bp.get("/<int:employee_id>/context")
def get_employee_context(employee_id):
    employee = TeamMember.query.get_or_404(employee_id)

    membership = (
        TeamMembership.query
        .filter_by(team_member_id=employee.id)
        .first()
    )

    if not membership:
        return jsonify({
            "employee_id": employee.id,
            "team_id": None,
            "section_id": None
        })

    team = Team.query.get(membership.team_id)

    return jsonify({
        "employee_id": employee.id,
        "team_id": team.id,
        "section_id": team.section_id
    })

@employees_bp.get("/section/<int:section_id>")
def get_employees_of_section(section_id):
    employees = (
        db.session.query(TeamMember)
        .join(TeamMembership)
        .join(Team)
        .filter(Team.section_id == section_id)
        .distinct()
        .all()
    )

    return jsonify([
        {
            "id": e.id,
            "first_name": e.first_name,
            "last_name": e.last_name
        }
        for e in employees
    ])

@employees_bp.get("/<int:employee_id>/context")
def get_employee_context(employee_id):
    employee = TeamMember.query.get_or_404(employee_id)

    membership = (
        TeamMembership.query
        .filter_by(team_member_id=employee.id)
        .first()
    )

    if not membership:
        return jsonify({
            "employee_id": employee.id,
            "team_id": None,
            "section_id": None
        })

    team = Team.query.get(membership.team_id)

    return jsonify({
        "employee_id": employee.id,
        "team_id": team.id,
        "section_id": team.section_id
    })

@employees_bp.post("/")
def create_employee():
    data = request.json
    employee = TeamMember(
        first_name=data["first_name"],
        last_name=data["last_name"],
        login=data["login"],
        password_hash=data["password"]
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify({"id": employee.id}), 201


@employees_bp.delete("/<int:employee_id>")
def fire_employee(employee_id):
    employee = TeamMember.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"status": "deleted"})


@employees_bp.get("/")
def get_all_employees():
    return jsonify([
        {
            "id": e.id,
            "first_name": e.first_name,
            "last_name": e.last_name
        } for e in TeamMember.query.all()
    ])

