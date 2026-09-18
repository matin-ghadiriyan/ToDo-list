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

from ..extensions import db
from ..forms import TaskForm
from ..models import Task

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/")
def list_tasks():
    """All tasks with optional filtering and search."""
    status = request.args.get("status", "all")
    q = request.args.get("q", "").strip()
    priority = request.args.get("priority", "all")

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
def today():
    """Tasks scheduled for today."""
    tasks = (
        Task.query.filter(Task.due_date == date.today())
        .order_by(Task.done.asc(), Task.priority.desc())
        .all()
    )
    return render_template("tasks/today.html", tasks=tasks)


@tasks_bp.route("/new", methods=["GET", "POST"])
def create():
    """Create a new task."""
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data.strip(),
            description=(form.description.data or "").strip(),
            priority=form.priority.data,
            due_date=form.due_date.data,
        )
        db.session.add(task)
        db.session.commit()
        flash("کار جدید با موفقیت اضافه شد.", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, task=None)


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
def edit(task_id: int):
    """Edit an existing task."""
    task = db.session.get(Task, task_id) or abort(404)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = (form.description.data or "").strip()
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash("تغییرات ذخیره شد.", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, task=task)


@tasks_bp.route("/<int:task_id>/toggle", methods=["POST"])
def toggle(task_id: int):
    """Flip the done state of a task."""
    task = db.session.get(Task, task_id) or abort(404)
    task.done = not task.done
    db.session.commit()
    return redirect(request.referrer or url_for("tasks.list_tasks"))


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
def delete(task_id: int):
    """Delete a task."""
    task = db.session.get(Task, task_id) or abort(404)
    db.session.delete(task)
    db.session.commit()
    flash("کار حذف شد.", "info")
    return redirect(request.referrer or url_for("tasks.list_tasks"))
