#!/usr/bin/env python3
"""
Entry point for the AI Knowledge Assistant Flask application
"""

from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
