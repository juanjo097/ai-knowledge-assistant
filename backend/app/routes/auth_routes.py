from flask import Blueprint, request, jsonify
from ..services.auth_service import verify_credentials, create_jwt

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user = data.get("username", "").strip()
    pwd = data.get("password", "")
    if not user or not pwd:
        return jsonify({"error": "username and password required"}), 400
    if not verify_credentials(user, pwd):
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"token": create_jwt(user)})
