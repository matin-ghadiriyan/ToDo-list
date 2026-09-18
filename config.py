"""Application configuration."""
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean from the environment."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    """Base configuration with security defaults."""

    ENV_NAME = os.environ.get("FLASK_ENV", "development")

    # --- Secrets & session ------------------------------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SESSION_COOKIE_NAME = "taskflow_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", False)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_REFRESH_EACH_REQUEST = True
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB request cap

    # --- CSRF -------------------------------------------------------------
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # tokens valid for 1 hour
    WTF_CSRF_SSL_STRICT = True

    # --- Database ---------------------------------------------------------
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "instance", "todo.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # --- Rate limiting ----------------------------------------------------
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_DEFAULT = "200 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STRATEGY = "fixed-window"

    # --- Misc -------------------------------------------------------------
    TASKS_PER_PAGE = 10
    MAX_SEARCH_LENGTH = 100


class DevelopmentConfig(Config):
    """Local development."""

    DEBUG = True
    ENV_NAME = "development"
    SESSION_COOKIE_SECURE = False
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production: secure cookies, HSTS, strict limits."""

    DEBUG = False
    ENV_NAME = "production"
    SESSION_COOKIE_SECURE = True
    RATELIMIT_ENABLED = True


class TestingConfig(Config):
    """Automated tests: no CSRF, no limiter, in-memory DB."""

    TESTING = True
    ENV_NAME = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    SECRET_KEY = "testing-secret-key-not-for-production"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
