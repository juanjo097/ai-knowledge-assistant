from __future__ import annotations
from flask import Flask


def register_routes(app: Flask):
    from .upload_routes import bp as upload_bp
    from .chunks_routes import bp as chunks_bp
    from .index_routes import bp as index_bp
    from .chat_routes import bp as chat_bp
    from .tools_routes import bp as tools_bp
    from .pipeline_routes import bp as pipeline_bp
    from .auth_routes import bp as auth_bp
    
    app.register_blueprint(upload_bp)
    app.register_blueprint(chunks_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(pipeline_bp)
    app.register_blueprint(auth_bp)
      
    
__all__ = ["register_routes"]
