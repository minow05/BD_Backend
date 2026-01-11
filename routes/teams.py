from flask import Blueprint, request, jsonify
from models import db, Team, TeamMembership, Task

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

@teams_bp.get("/")
def get_teams():
    teams = Team.query.all()

    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "section_id": t.section_id
        }
        for t in teams
    ])

@teams_bp.get("/section/<int:section_id>")
def get_teams_of_section(section_id):
    teams = Team.query.filter_by(section_id=section_id).all()

    return jsonify([
        {
            "id": t.id,
            "name": t.name
        }
        for t in teams
    ])

@teams_bp.get("/<int:team_id>/progress")
def get_team_progress(team_id):
    total_tasks = Task.query.filter_by(assigned_team_id=team_id).count()

    completed_tasks = (
        Task.query
        .filter_by(assigned_team_id=team_id, status="DONE")
        .count()
    )

    return jsonify({
        "team_id": team_id,
        "completed": completed_tasks,
        "total": total_tasks,
        "progress_percent": (
            round((completed_tasks / total_tasks) * 100, 2)
            if total_tasks > 0 else 0
        )
    })
