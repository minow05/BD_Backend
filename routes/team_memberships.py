from flask import Blueprint, request, jsonify
from models import (
    db, TeamMembership
)

team_memberships_bp = Blueprint("team_memberships", __name__)

@team_memberships_bp.post("/")
def add_employee_to_team():
    data = request.json
    membership = TeamMembership(
        employee_id=data["employee_id"],
        team_id=data["team_id"]
    )
    db.session.add(membership)
    db.session.commit()
    return jsonify({"status": "ok"}), 201


@team_memberships_bp.delete("/<int:employee_id>/<int:team_id>")
def remove_employee_from_team(employee_id, team_id):
    membership = TeamMembership.query.filter_by(
        employee_id=employee_id,
        team_id=team_id
    ).first_or_404()

    db.session.delete(membership)
    db.session.commit()
    return jsonify({"status": "removed"})

