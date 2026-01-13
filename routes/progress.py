from flask import Blueprint, request, jsonify
from models import (
    db, Task, TeamTask, TaskStatus
)

progress_bp = Blueprint("progress", __name__)\

@progress_bp.get("/teams/<int:team_id>")
def team_progress(team_id):
    total = (
        db.session.query(Task)
        .join(TeamTask)
        .filter(TeamTask.team_id == team_id)
        .count()
    )

    done = (
        db.session.query(Task)
        .join(TeamTask)
        .filter(
            TeamTask.team_id == team_id,
            Task.status == TaskStatus.DONE
        )
        .count()
    )

    return jsonify({
        "completed": done,
        "total": total,
        "progress_percent": round((done / total) * 100, 2) if total else 0
    })
