"""Shared pytest fixtures."""
import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture()
def app():
    """Create a test application with an in-memory database."""
    test_app = create_app("testing")
    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    """A Flask test client bound to the test app."""
    return app.test_client()
