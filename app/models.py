"""Database models."""
from datetime import datetime, date

from .extensions import db


class Task(db.Model):
    """A single to-do task."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    priority = db.Column(db.String(10), default="normal", nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @property
    def is_today(self) -> bool:
        """Whether the task is scheduled for today."""
        return self.due_date == date.today()

    @property
    def is_overdue(self) -> bool:
        """Whether the task is past due and not completed."""
        return bool(
            self.due_date and self.due_date < date.today() and not self.done
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Task {self.id} {self.title!r}>"
