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

    task = Task(
        description=data["description"],
        status=TaskStatus.TODO
    )
    team_task = TeamTask(
        task_id=task.id,
        section_task_id=data["section_task_id"],
        team_id=data["team_id"]
    )

    db.session.add(team_task)
    db.session.commit()

    return jsonify({"id": team_task.id}), 201


@tasks_bp.post("/employee")
def create_employee_task():
    data = request.json

    task = Task(
        description=data["description"],
        status=TaskStatus.TODO
    )
    employee_task = EmployeeTask(
        task_id=task.id,
        team_task_id=data["team_task_id"],
        team_member_id=data["team_member_id"]
    )

    db.session.add(employee_task)
    db.session.commit()

    return jsonify({"id": employee_task.id}), 201

@tasks_bp.get("/employee/<int:employee_id>")
def get_tasks_for_employee(employee_id):
    tasks = (
        db.session.query(Task)
        .join(EmployeeTask, EmployeeTask.task_id == Task.id)
        .filter(EmployeeTask.team_member_id == employee_id)
        .all()
    )

    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "status": t.status.value
        }
        for t in tasks
    ])

@tasks_bp.get("/team/<int:team_id>")
def get_tasks_for_team(team_id):
    tasks = (
        db.session.query(Task)
        .join(TeamTask, TeamTask.task_id == Task.id)
        .filter(TeamTask.team_id == team_id)
        .all()
    )

    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "status": t.status.value
        }
        for t in tasks
    ])

@tasks_bp.get("/section/<int:section_id>")
def get_tasks_for_section(section_id):
    tasks = (
        db.session.query(Task)
        .join(SectionTask, SectionTask.task_id == Task.id)
        .filter(SectionTask.section_id == section_id)
        .all()
    )

    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "status": t.status.value
        }
        for t in tasks
    ])

@tasks_bp.get("/")
def get_all_tasks():
    tasks = Task.query.all()

    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "status": t.status.value
        }
        for t in tasks
    ])

@tasks_bp.get("/<int:task_id>")
def get_task_details(task_id):
    task = Task.query.get_or_404(task_id)

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "assigned_team_id": task.assigned_team_id
    })

@tasks_bp.patch("/<int:task_id>/status")
def update_task_status(task_id):
    data = request.json
    task = Task.query.get_or_404(task_id)
    task.status = TaskStatus[data["status"]]
    db.session.commit()
    return jsonify({"status": "updated"})


