from __future__ import annotations
from flask import Flask


def register_routes(app: Flask):
    from .upload import bp as upload_bp
    app.register_blueprint(upload_bp)