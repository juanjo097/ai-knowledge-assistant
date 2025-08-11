from flask import request, jsonify
from ..services.auth_service import verify_jwt

PUBLIC_PATHS = ("/auth/login", "/health")

def auth_middleware(app):
    @app.before_request
    def _check_auth():
        p = request.path
        if any(p.startswith(x) for x in PUBLIC_PATHS):
            return
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing bearer token"}), 401
        token = auth.split(" ", 1)[1]
        if not verify_jwt(token):
            return jsonify({"error": "invalid or expired token"}), 401