from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import Settings
from config.database import init_db
from error_handlers import register_error_handlers
import logging
from .routes import register_routes

def create_app():
    # Load environment variables
    load_dotenv(override=False)
    
    # Build settings
    settings = Settings.from_env()
    
    app = Flask(__name__)
    
    # Basic configuration
    app.config["MAX_CONTENT_LENGTH"] = settings.max_content_length_bytes
    
    # CORS configuration
    CORS(app, origins=settings.CORS_ORIGINS)
    
    # Store settings for later use
    app.config["SETTINGS"] = settings
    
    # Initialize database (after settings are stored)
    init_db(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register routes
    register_routes(app)
    
    # Basic logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s - %(message)s",
    )
    
    @app.route("/", methods=["GET"])
    def root():
        return jsonify({
            "message": "AI Knowledge Assistant API",
            "version": "1.0.0",
            "status": "running"
        }), 200
    
    @app.route("/health", methods=["GET"]) 
    def health():
        return jsonify({
            "status": "ok",
            "data_dir": settings.DATA_DIR,
            "db": settings.DB_URL,
            "max_upload_mb": settings.MAX_UPLOAD_MB,
        }), 200
    
    return app



# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

