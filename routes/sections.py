from flask import Blueprint, request, jsonify
from models import db, Section

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
