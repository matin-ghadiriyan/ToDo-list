"""Application factory."""
import os

from flask import Flask

from config import config
from .extensions import db, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure a Flask application instance."""
    config_name = config_name or os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure the instance folder exists (SQLite lives there).
    os.makedirs(app.instance_path, exist_ok=True)

    # Bind extensions.
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints.
    from .routes.main import main_bp
    from .routes.tasks import tasks_bp
    from .routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(api_bp, url_prefix="/api")

    # Jinja helpers.
    @app.context_processor
    def inject_globals():
        from datetime import datetime

        return {"now": datetime.utcnow()}

    @app.template_filter("fa_date")
    def fa_date(value):
        """Format a date in a readable ISO-like form."""
        if not value:
            return "—"
        return value.strftime("%Y-%m-%d")

    # Create tables automatically (handy for first run without migrations).
    with app.app_context():
        db.create_all()

    return app
