"""Security-focused tests."""
from app.extensions import db as _db
from app.models import Task
from app.security import is_safe_url, sanitize_text


# --------------------------------------------------------------------------- #
# sanitize_text
# --------------------------------------------------------------------------- #


def test_sanitize_strips_script_tags():
    dirty = '<script>alert("xss")</script>سلام'
    cleaned = sanitize_text(dirty)
    assert "<script>" not in cleaned
    assert "alert" not in cleaned
    assert "سلام" in cleaned


def test_sanitize_strips_img_onerror():
    dirty = '<img src=x onerror=alert(1)>'
    cleaned = sanitize_text(dirty)
    assert "<img" not in cleaned
    assert "onerror" not in cleaned


def test_sanitize_removes_control_chars():
    dirty = "hello\x00world\x07"
    cleaned = sanitize_text(dirty)
    assert "\x00" not in cleaned
    assert "\x07" not in cleaned
    assert "helloworld" in cleaned


def test_sanitize_clamps_length():
    long_text = "a" * 5000
    assert len(sanitize_text(long_text, max_length=200)) == 200


def test_sanitize_handles_none_and_empty():
    assert sanitize_text(None) == ""
    assert sanitize_text("") == ""


# --------------------------------------------------------------------------- #
# is_safe_url (open-redirect protection)
# --------------------------------------------------------------------------- #


def test_is_safe_url_rejects_external(app):
    with app.test_request_context("/"):
        assert is_safe_url("https://evil.example.com/steal") is False
        assert is_safe_url("//evil.example.com") is False


def test_is_safe_url_accepts_relative(app):
    with app.test_request_context("/"):
        assert is_safe_url("/tasks/") is True


def test_is_safe_url_rejects_empty(app):
    with app.test_request_context("/"):
        assert is_safe_url(None) is False
        assert is_safe_url("") is False


# --------------------------------------------------------------------------- #
# Security headers
# --------------------------------------------------------------------------- #


def test_security_headers_present(client):
    response = client.get("/")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert "Content-Security-Policy" in response.headers
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_server_header_hidden(client):
    response = client.get("/")
    assert "Server" not in response.headers


# --------------------------------------------------------------------------- #
# Stored XSS via the create form
# --------------------------------------------------------------------------- #


def test_create_task_rejects_html(client, app):
    """The form validator must reject raw HTML in the title."""
    response = client.post(
        "/tasks/new",
        data={"title": "<script>alert(1)</script>", "priority": "normal"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert Task.query.count() == 0


# --------------------------------------------------------------------------- #
# Invalid task IDs
# --------------------------------------------------------------------------- #


def test_toggle_unknown_task_returns_404(client):
    assert client.post("/tasks/99999/toggle").status_code == 404


def test_delete_unknown_task_returns_404(client):
    assert client.post("/tasks/99999/delete").status_code == 404


# --------------------------------------------------------------------------- #
# Error pages
# --------------------------------------------------------------------------- #


def test_404_page_for_unknown_route(client):
    assert client.get("/this-does-not-exist").status_code == 404
