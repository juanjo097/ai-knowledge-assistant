from __future__ import annotations
from flask import Flask


def register_routes(app: Flask):
    from .upload_routes import bp as upload_bp
    from .chunks_routes import bp as chunks_bp
    from .index_routes import bp as index_bp
    
    app.register_blueprint(upload_bp)
    app.register_blueprint(chunks_bp)
    app.register_blueprint(index_bp)
    
    
__all__ = ["register_routes"]
