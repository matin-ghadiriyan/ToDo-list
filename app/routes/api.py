"""JSON API endpoints (used by the JavaScript layer)."""
from flask import Blueprint, jsonify, request, abort

from ..extensions import db, limiter
from ..models import Task
from ..security import sanitize_text

api_bp = Blueprint("api", __name__)


@api_bp.route("/tasks")
@limiter.limit("90 per minute")
def get_tasks():
    """Return all tasks as JSON."""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@api_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
@limiter.limit("120 per minute")
def update_task(task_id: int):
    """Partially update a task (used for quick toggles)."""
    # CSRF is enforced by the global CSRFProtect; JSON clients must send
    # the X-CSRFToken header. See app.js for the client-side hook.
    task = db.session.get(Task, task_id)
    if not task:
        abort(404)

    data = request.get_json(silent=True) or {}
    if "done" in data:
        task.done = bool(data["done"])
    if "title" in data and data["title"]:
        task.title = sanitize_text(data["title"], max_length=200)

    db.session.commit()
    return jsonify(task.to_dict())
