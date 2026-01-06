from flask import Blueprint, request, jsonify
from models import db, Employee, TeamMember

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
