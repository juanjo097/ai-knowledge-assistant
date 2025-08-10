from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import Settings
import logging

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
    
    # Basic logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s - %(message)s",
    )
    
    # Store settings for later use
    app.config["SETTINGS"] = settings
    
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

