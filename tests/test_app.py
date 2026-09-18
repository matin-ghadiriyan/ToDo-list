"""Basic tests for the ToDo application."""
from app.extensions import db as _db
from app.models import Task


def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create_task(client, app):
    response = client.post(
        "/tasks/new",
        data={"title": "خرید نان", "priority": "normal"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert Task.query.count() == 1
        assert Task.query.first().title == "خرید نان"


def test_toggle_task(client, app):
    with app.app_context():
        task = Task(title="تست", done=False)
        _db.session.add(task)
        _db.session.commit()
        task_id = task.id

    client.post(f"/tasks/{task_id}/toggle")
    with app.app_context():
        assert _db.session.get(Task, task_id).done is True


def test_delete_task(client, app):
    with app.app_context():
        task = Task(title="حذف شدنی")
        _db.session.add(task)
        _db.session.commit()
        task_id = task.id

    client.post(f"/tasks/{task_id}/delete")
    with app.app_context():
        assert _db.session.get(Task, task_id) is None


def test_api_tasks(client, app):
    with app.app_context():
        _db.session.add(Task(title="از طریق API"))
        _db.session.commit()

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "از طریق API"
