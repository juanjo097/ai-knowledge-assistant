"""
Environment-specific settings and constants.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Environment
ENVIRONMENT = os.environ.get('FLASK_ENV', 'development')

# Flask settings
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', '1' if ENVIRONMENT == 'development' else '0')
FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))

# Database settings
DATABASE_PATH = BASE_DIR / 'data'
DATABASE_FILE = DATABASE_PATH / 'app.db'

# Upload settings
UPLOAD_PATH = BASE_DIR / 'uploads'
TEMP_PATH = BASE_DIR / 'temp'

# Log settings
LOG_PATH = BASE_DIR / 'logs'
LOG_FILE = LOG_PATH / 'app.log'

# AI Service settings
AI_SERVICES = {
    'openai': {
        'enabled': bool(os.environ.get('OPENAI_API_KEY')),
        'model': os.environ.get('OPENAI_MODEL', 'gpt-4'),
        'max_tokens': int(os.environ.get('OPENAI_MAX_TOKENS', 4000)),
        'temperature': float(os.environ.get('OPENAI_TEMPERATURE', 0.7))
    },
    'anthropic': {
        'enabled': bool(os.environ.get('ANTHROPIC_API_KEY')),
        'model': os.environ.get('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229'),
        'max_tokens': int(os.environ.get('ANTHROPIC_MAX_TOKENS', 4000))
    }
}

# Security settings
SECURITY_SETTINGS = {
    'password_min_length': 8,
    'session_timeout': 3600,  # 1 hour
    'max_login_attempts': 5,
    'lockout_duration': 900,  # 15 minutes
}

# Rate limiting
RATE_LIMIT = {
    'default': '100 per minute',
    'auth': '5 per minute',
    'api': '1000 per hour'
}

# File processing
FILE_PROCESSING = {
    'max_file_size': 16 * 1024 * 1024,  # 16MB
    'allowed_extensions': {
        'text': {'.txt', '.md', '.rst'},
        'documents': {'.pdf', '.doc', '.docx', '.rtf'},
        'images': {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'},
    },
    'text_extraction': {
        'pdf': True,
        'doc': False,  # Requires additional libraries
        'docx': True,
        'images': False  # Requires OCR
    }
}

# Knowledge base settings
KNOWLEDGE_BASE = {
    'max_documents': 10000,
    'max_document_size': 10 * 1024 * 1024,  # 10MB
    'search_results_limit': 50,
    'embedding_model': 'text-embedding-ada-002',
    'chunk_size': 1000,
    'chunk_overlap': 200
}
