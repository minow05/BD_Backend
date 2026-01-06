from flask import Blueprint, request, jsonify
from models import db, Team, TeamMembership

teams_bp = Blueprint("teams", __name__)


@teams_bp.post("/")
def create_team():
    data = request.json

    team = Team(
        name=data["name"],
        section_id=data["section_id"],
        manager_id=data["manager_id"]
    )

    db.session.add(team)
    db.session.commit()

    return jsonify({"id": team.id}), 201


@teams_bp.post("/add-member")
def add_member():
    data = request.json

    membership = TeamMembership(
        team_id=data["team_id"],
        team_member_id=data["team_member_id"]
    )

    db.session.add(membership)
    db.session.commit()

    return jsonify({"status": "ok"}), 201
