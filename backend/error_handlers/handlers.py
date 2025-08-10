"""
Simple error handlers for the AI Knowledge Assistant API.
"""

from flask import Flask, jsonify
from .exceptions import APIError, ValidationError, NotFoundError, FileTooLargeError


def register_error_handlers(app: Flask) -> None:
    """Register error handlers with the Flask application."""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            'success': False,
            'error': error.message,
            'status_code': 400
        }), 400
    
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        return jsonify({
            'success': False,
            'error': error.message,
            'status_code': 404
        }), 404
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = {
            'success': False,
            'error': error.message,
            'status_code': error.status_code
        }
        if error.extra:
            response['extra'] = error.extra
        return jsonify(response), error.status_code
    
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'status_code': 500
        }), 500

    @app.errorhandler(FileTooLargeError)
    def handle_file_too_large_error(error):
        return jsonify({
            'success': False,
            'error': error.message,
            'status_code': 413
        }), 413