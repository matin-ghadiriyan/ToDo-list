"""Application factory with security hardening."""
import os

from flask import Flask, jsonify, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

from config import config
from .extensions import db, migrate, csrf, limiter
from .security import apply_security_headers, validate_secret_key


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure a hardened Flask application instance."""
    config_name = config_name or os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config["ENV_NAME"] = app.config.get("ENV_NAME", config_name)

    is_production = app.config["ENV_NAME"] == "production"

    # Refuse to boot in production with a weak secret key.
    validate_secret_key(app)

    # Respect X-Forwarded-* headers when behind a reverse proxy.
    if is_production:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # Ensure the instance folder exists (SQLite lives there).
    os.makedirs(app.instance_path, exist_ok=True)

    # --- Extensions ------------------------------------------------------ #
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    # --- Blueprints ------------------------------------------------------ #
    from .routes.main import main_bp
    from .routes.tasks import tasks_bp
    from .routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(api_bp, url_prefix="/api")

    # --- Jinja helpers --------------------------------------------------- #
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

    # --- Security headers on every response ------------------------------ #
    @app.after_request
    def _security_headers(response):
        return apply_security_headers(response, is_production=is_production)

    # --- Error handlers -------------------------------------------------- #
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith("/api/"):
            return jsonify(error="درخواست نامعتبر"), 400
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(error):
        if request.path.startswith("/api/"):
            return jsonify(error="دسترسی مجاز نیست"), 403
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify(error="یافت نشد"), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(429)
    def ratelimit_handler(error):
        if request.path.startswith("/api/"):
            return jsonify(error="تعداد درخواست‌ها بیش از حد مجاز"), 429
        return render_template("errors/429.html"), 429

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith("/api/"):
            return jsonify(error="خطای داخلی سرور"), 500
        return render_template("errors/500.html"), 500

    # --- Create tables automatically (first run without migrations) ------- #
    with app.app_context():
        db.create_all()

    return app
