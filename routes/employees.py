from flask import Blueprint, request, jsonify
from models import db, Employee, TeamMember, TeamMembership, Team, StudioHead, SectionManager, TeamManager, Section
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

employees_bp = Blueprint("employees", __name__)

@employees_bp.post("/")
def create_employee():
    data = request.json

    employee = TeamMember(
        first_name=data["first_name"],
        last_name=data["last_name"],
        pesel=data["pesel"],
        phone=data ["phone"],
        login=data["login"],
        hire_date = str(date.today()),
        password_hash=generate_password_hash(data["password"])
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({"id": employee.id}), 201

@employees_bp.get("/team-member")
def get_teammember():
    employees = Employee.query.all()
    
    # Pobierz wszystkie ID z każdej tabeli specjalizacji
    studio_head_ids = {sh.id for sh in StudioHead.query.all()}
    section_manager_ids = {sm.id for sm in SectionManager.query.all()}
    team_manager_ids = {tm.id for tm in TeamManager.query.all()}
    
    result = []
    for employee in employees:
        position = "pracownik"
        employee_id = employee.id
        
        if employee_id in studio_head_ids:
            continue
        elif employee_id in section_manager_ids:
            continue
        elif employee_id in team_manager_ids:
            continue
        
        result.append({
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "pesel": employee.pesel,
            "phone": employee.phone,
            "hire_date": employee.hire_date,
            "fire_date": employee.fire_date,
            "position": position
        })

@employees_bp.get("/")
def get_employees():
    employees = Employee.query.all()
    
    studio_head_ids = {sh.id for sh in StudioHead.query.all()}
    section_manager_ids = {sm.id for sm in SectionManager.query.all()}
    team_manager_ids = {tm.id for tm in TeamManager.query.all()}
    
    result = []
    for employee in employees:
        position = "pracownik"
        employee_id = employee.id
        
        if employee_id in studio_head_ids:
            continue
        elif employee_id in section_manager_ids:
            position = "kierownik sekcji"
        elif employee_id in team_manager_ids:
            position = "kierownik zespołu"
        
        result.append({
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "pesel": employee.pesel,
            "phone": employee.phone,
            "hire_date": employee.hire_date,
            "fire_date": employee.fire_date,
            "position": position
        })
    
    return jsonify(result)
@employees_bp.get("/employee/<int:id>")
def get_employee_id(id):

    employeee = (
        db.session.query(Employee)
        .filter(Employee.id == id)
    )
    for employee in employeee:
        position = "pracownik"
        studioHead = StudioHead.query.all()
        sectionManager = SectionManager.query.all()
        teamManager = TeamManager.query.all()
        id = employee.id
        for e in teamManager:
            if id == e.id:
                position = "kierownik zespołu"
        for e in sectionManager:
            if id == e.id:
                position = "kierownik sekcji"
        for e in studioHead:
            if id == e.id:
                position = "szef studia"
    return jsonify([
        {
            "id": employee.id,
            "position": position,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "pesel": employee.pesel,
            "phone": employee.phone,
            "hire_date": employee.hire_date,
            "login": employee.login,
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

@employees_bp.get("/<int:team_member_id>/context")
def get_employee_context(team_member_id):
    # team jako członek
    membership = TeamMembership.query.filter_by(team_member_id=team_member_id).first()

    if membership:
        team = Team.query.get(membership.team_id)
        return jsonify({
            "employee_id": team_member_id,
            "team_id": team.id,
            "section_id": team.section_id,
            "role": "TEAM_MEMBER"
        })

    # team jako manager
    team = Team.query.filter_by(manager_id=team_member_id).first()
    if team:
        return jsonify({
            "employee_id": team_member_id,
            "team_id": team.id,
            "section_id": team.section_id,
            "role": "TEAM_MANAGER"
        })

    # section jako manager
    section = Section.query.filter_by(manager_id=team_member_id).first()
    if section:
        return jsonify({
            "employee_id": team_member_id,
            "team_id": None,
            "section_id": section.id,
            "role": "SECTION_MANAGER"
        })

    return jsonify({
        "employee_id": team_member_id,
        "team_id": None,
        "section_id": None,
        "role": "NONE"
    })



@employees_bp.delete("/<int:employee_id>")
def fire_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
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

