"""Task CRUD pages."""
from datetime import date

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
)

from ..extensions import db, limiter
from ..forms import TaskForm
from ..models import Task
from ..security import safe_redirect_target, sanitize_text

tasks_bp = Blueprint("tasks", __name__)

# Whitelisted values keep the query-string surface small.
_ALLOWED_STATUS = {"all", "done", "pending"}
_ALLOWED_PRIORITY = {"all", "low", "normal", "high"}


@tasks_bp.route("/")
@limiter.limit("60 per minute")
def list_tasks():
    """All tasks with optional filtering and search."""
    status = request.args.get("status", "all")
    priority = request.args.get("priority", "all")
    q = sanitize_text(request.args.get("q", ""), max_length=100)

    # Reject anything outside the whitelist instead of passing it to the DB.
    if status not in _ALLOWED_STATUS:
        status = "all"
    if priority not in _ALLOWED_PRIORITY:
        priority = "all"

    query = Task.query

    if status == "done":
        query = query.filter(Task.done.is_(True))
    elif status == "pending":
        query = query.filter(Task.done.is_(False))

    if priority in {"low", "normal", "high"}:
        query = query.filter(Task.priority == priority)

    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Task.title.ilike(like), Task.description.ilike(like))
        )

    tasks = query.order_by(Task.done.asc(), Task.created_at.desc()).all()
    return render_template(
        "tasks/list.html",
        tasks=tasks,
        status=status,
        q=q,
        priority=priority,
    )


@tasks_bp.route("/today")
@limiter.limit("60 per minute")
def today():
    """Tasks scheduled for today."""
    tasks = (
        Task.query.filter(Task.due_date == date.today())
        .order_by(Task.done.asc(), Task.priority.desc())
        .all()
    )
    return render_template("tasks/today.html", tasks=tasks)


@tasks_bp.route("/new", methods=["GET", "POST"])
@limiter.limit("20 per minute", methods=["POST"])
def create():
    """Create a new task."""
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=sanitize_text(form.title.data, max_length=200),
            description=sanitize_text(form.description.data, max_length=2000),
            priority=form.priority.data,
            due_date=form.due_date.data,
        )
        db.session.add(task)
        db.session.commit()
        flash("کار جدید با موفقیت اضافه شد.", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, task=None)


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@limiter.limit("30 per minute", methods=["POST"])
def edit(task_id: int):
    """Edit an existing task."""
    task = db.session.get(Task, task_id) or abort(404)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = sanitize_text(form.title.data, max_length=200)
        task.description = sanitize_text(form.description.data, max_length=2000)
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash("تغییرات ذخیره شد.", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, task=task)


@tasks_bp.route("/<int:task_id>/toggle", methods=["POST"])
@limiter.limit("120 per minute")
def toggle(task_id: int):
    """Flip the done state of a task."""
    task = db.session.get(Task, task_id) or abort(404)
    task.done = not task.done
    db.session.commit()
    # Open-redirect safe: only same-host referrers are honoured.
    return redirect(safe_redirect_target(url_for("tasks.list_tasks")))


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@limiter.limit("30 per minute")
def delete(task_id: int):
    """Delete a task."""
    task = db.session.get(Task, task_id) or abort(404)
    db.session.delete(task)
    db.session.commit()
    flash("کار حذف شد.", "info")
    return redirect(safe_redirect_target(url_for("tasks.list_tasks")))
