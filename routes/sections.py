from flask import Blueprint, request, jsonify
from models import db, Section, Team, Task


sections_bp = Blueprint("sections", __name__)


@sections_bp.post("/")
def create_section():
    data = request.json

    section = Section(
        name=data["name"],
        manager_id=data["manager_id"]
    )

    db.session.add(section)
    db.session.commit()

    return jsonify({"id": section.id}), 201


@sections_bp.get("/")
def get_sections():
    sections = Section.query.all()

    return jsonify([
        {
            "id": s.id,
            "name": s.name
        }
        for s in sections
    ])

@sections_bp.get("/<int:section_id>")
def get_section_details(section_id):
    section = Section.query.get_or_404(section_id)

    teams = Team.query.filter_by(section_id=section.id).all()

    return jsonify({
        "id": section.id,
        "name": section.name,
        "manager_id": section.manager_id,
        "teams": [
            {
                "id": t.id,
                "name": t.name
            } for t in teams
        ]
    })

@sections_bp.get("/<int:section_id>/progress")
def get_section_progress(section_id):
    total_tasks = (
        db.session.query(Task)
        .join(Team)
        .filter(Team.section_id == section_id)
        .count()
    )

    completed_tasks = (
        db.session.query(Task)
        .join(Team)
        .filter(
            Team.section_id == section_id,
            Task.status == "DONE"
        )
        .count()
    )

    return jsonify({
        "section_id": section_id,
        "completed": completed_tasks,
        "total": total_tasks,
        "progress_percent": (
            round((completed_tasks / total_tasks) * 100, 2)
            if total_tasks > 0 else 0
        )
    })

@sections_bp.get("/<int:section_id>/teams")
def get_teams_of_section(section_id):
    teams = Team.query.filter_by(section_id=section_id).all()
    return jsonify([
        {"id": t.id, "name": t.name}
        for t in teams
    ])
