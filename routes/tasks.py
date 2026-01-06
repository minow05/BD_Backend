from flask import Blueprint, request, jsonify
from models import (
    db, Task, SectionTask, TeamTask, EmployeeTask, TaskStatus
)

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.post("/section")
def create_section_task():
    data = request.json

    task = Task(
        description=data["description"],
        status=TaskStatus.TODO
    )
    db.session.add(task)
    db.session.flush()

    section_task = SectionTask(
        task_id=task.id,
        section_id=data["section_id"],
        game_id=data["game_id"]
    )

    db.session.add(section_task)
    db.session.commit()

    return jsonify({"task_id": task.id}), 201


@tasks_bp.post("/team")
def create_team_task():
    data = request.json

    team_task = TeamTask(
        section_task_id=data["section_task_id"],
        team_id=data["team_id"]
    )

    db.session.add(team_task)
    db.session.commit()

    return jsonify({"id": team_task.id}), 201


@tasks_bp.post("/employee")
def create_employee_task():
    data = request.json

    employee_task = EmployeeTask(
        team_task_id=data["team_task_id"],
        team_member_id=data["team_member_id"]
    )

    db.session.add(employee_task)
    db.session.commit()

    return jsonify({"id": employee_task.id}), 201
