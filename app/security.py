"""Security helpers: sanitization, safe redirects, security headers."""
from __future__ import annotations

import os
import re
from urllib.parse import urljoin, urlparse

import bleach
from flask import Response, request

# --------------------------------------------------------------------------- #
# Input sanitization
# --------------------------------------------------------------------------- #

ALLOWED_TAGS: list[str] = []  # no HTML at all in task text
ALLOWED_ATTRIBUTES: dict[str, list[str]] = {}

# Control characters except \n and \t
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_text(value: str | None, *, max_length: int = 2000) -> str:
    """Strip HTML/control chars and clamp length.

    This is the single entry point for all user-supplied task text and
    protects against stored XSS in addition to Jinja's autoescaping.
    """
    if not value:
        return ""
    cleaned = bleach.clean(
        str(value),
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )
    cleaned = _CONTROL_CHARS.sub("", cleaned)
    cleaned = cleaned.replace("\r\n", "\n").strip()
    return cleaned[:max_length]


# --------------------------------------------------------------------------- #
# Safe redirects (open-redirect protection)
# --------------------------------------------------------------------------- #


def is_safe_url(target: str | None) -> bool:
    """Return True only for same-host relative URLs."""
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def safe_redirect_target(fallback: str) -> str:
    """Return a validated Referer or the fallback endpoint path."""
    referrer = request.referrer
    if referrer and is_safe_url(referrer):
        return referrer
    return fallback


# --------------------------------------------------------------------------- #
# Security headers
# --------------------------------------------------------------------------- #

DEFAULT_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "object-src 'none'"
)


def apply_security_headers(response: Response, *, is_production: bool = False) -> Response:
    """Attach hardening headers to every response."""
    response.headers.setdefault("Content-Security-Policy", DEFAULT_CSP)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault(
        "Permissions-Policy",
        "geolocation=(), microphone=(), camera=(), payment=()",
    )
    response.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
    response.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
    response.headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")
    if is_production:
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains; preload",
        )
    # Never leak the framework signature.
    response.headers.pop("Server", None)
    return response


def validate_secret_key(app) -> None:
    """Fail fast if a production build uses a weak/default secret key."""
    weak_defaults = {
        "",
        "dev-secret-key-change-me",
        "change-me-to-a-random-secret",
        "secret",
        "changeme",
    }
    key = app.config.get("SECRET_KEY") or ""
    if app.config.get("ENV_NAME") == "production":
        if key in weak_defaults or len(key) < 32:
            raise RuntimeError(
                "SECRET_KEY must be a unique random value of at least 32 chars "
                "in production. Set the SECRET_KEY environment variable."
            )


def generate_secret_key() -> str:
    """Convenience helper to create a strong secret key."""
    return os.urandom(48).hex()
