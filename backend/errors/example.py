"""
Simple example of using the error handling system.
"""

from flask import Blueprint, request, jsonify
from .exceptions import ValidationError, NotFoundError

# Example blueprint
bp = Blueprint('example', __name__)


@bp.route('/users', methods=['POST'])
def create_user():
    """Example endpoint with validation error handling."""
    data = request.get_json()
    
    if not data:
        raise ValidationError("Request body is required")
    
    if 'username' not in data:
        raise ValidationError("Username is required")
    
    if 'email' not in data:
        raise ValidationError("Email is required")
    
    # Simulate user creation
    user = {"id": "123", "username": data['username'], "email": data['email']}
    
    return jsonify({
        "success": True,
        "data": user
    }), 201


@bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Example endpoint with not found error handling."""
    # Simulate user lookup
    if user_id == "999":
        raise NotFoundError("User not found")
    
    user = {"id": user_id, "username": "example_user", "email": "user@example.com"}
    return jsonify({"success": True, "data": user})


# To use this blueprint in your main app:
# from error_handlers.example import bp
# app.register_blueprint(bp, url_prefix='/api')
