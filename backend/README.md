# AI Knowledge Assistant - Backend

This is the Flask-based backend for the AI Knowledge Assistant application.

## Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

## Running the Application

**Development mode:**
```bash
python run.py
```

**Using Flask CLI:**
```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

The application will be available at `http://localhost:5000`

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Project Structure

```
backend/
├── app/
│   └── __init__.py      # Flask app factory and configuration
├── config/              # Configuration package
│   ├── __init__.py      # Configuration package init
│   ├── config.py        # Environment-specific config classes
│   └── settings.py      # Application settings and constants
├── data/                # Database and data files
├── uploads/             # File upload directory
├── temp/                # Temporary files
├── logs/                # Application logs
├── run.py               # Application entry point
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
└── README.md            # This file
```
