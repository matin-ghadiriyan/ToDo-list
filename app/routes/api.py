"""JSON API endpoints (used by the JavaScript layer)."""
from flask import Blueprint, jsonify, request, abort

from ..extensions import db
from ..models import Task

api_bp = Blueprint("api", __name__)


@api_bp.route("/tasks")
def get_tasks():
    """Return all tasks as JSON."""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@api_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id: int):
    """Partially update a task (used for quick toggles)."""
    task = db.session.get(Task, task_id)
    if not task:
        abort(404)

    data = request.get_json(silent=True) or {}
    if "done" in data:
        task.done = bool(data["done"])
    if "title" in data and data["title"]:
        task.title = str(data["title"]).strip()

    db.session.commit()
    return jsonify(task.to_dict())
