"""Dashboard / general pages."""
from datetime import date

from flask import Blueprint, render_template
from sqlalchemy import func

from ..extensions import db, limiter
from ..models import Task

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@limiter.limit("120 per minute")
def dashboard():
    """Overview page with statistics and recent tasks."""
    total = db.session.query(func.count(Task.id)).scalar() or 0
    done = (
        db.session.query(func.count(Task.id)).filter(Task.done.is_(True)).scalar()
        or 0
    )
    pending = total - done
    today = date.today()
    today_count = (
        db.session.query(func.count(Task.id))
        .filter(Task.due_date == today)
        .scalar()
        or 0
    )
    overdue = (
        db.session.query(func.count(Task.id))
        .filter(Task.due_date < today, Task.done.is_(False))
        .scalar()
        or 0
    )

    recent = Task.query.order_by(Task.created_at.desc()).limit(5).all()
    progress = int((done / total) * 100) if total else 0

    stats = {
        "total": total,
        "done": done,
        "pending": pending,
        "today": today_count,
        "overdue": overdue,
        "progress": progress,
    }
    return render_template("dashboard.html", stats=stats, recent=recent)


@main_bp.route("/about")
@limiter.limit("60 per minute")
def about():
    """About the project."""
    return render_template("about.html")
